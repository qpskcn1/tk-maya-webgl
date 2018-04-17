# Copyright (c) 2017 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.

import os
import sgtk
import tempfile
import datetime
import maya.cmds as cmds
import maya.mel as mel
from sgtk.platform.qt import QtCore, QtGui

from .ui.dialog import Ui_Dialog

logger = sgtk.platform.get_logger(__name__)

overlay = sgtk.platform.import_framework("tk-framework-qtwidgets", "overlay_widget")
sg_data = sgtk.platform.import_framework("tk-framework-shotgunutils", "shotgun_data")
task_manager = sgtk.platform.import_framework("tk-framework-shotgunutils", "task_manager")


class Dialog(QtGui.QWidget):
    """
    Main dialog window for the App
    """

    (DATA_ENTRY_UI, UPLOAD_COMPLETE_UI) = range(2)

    def __init__(self, parent=None):
        """
        :param parent: The parent QWidget for this control
        """
        QtGui.QWidget.__init__(self, parent)

        self._bundle = sgtk.platform.current_bundle()
        self._context = self._bundle.context
        self._publish_path = self._generate_path()
        self._title = os.path.basename(self._publish_path)
        self._thumbnail = None

        self._task_manager = task_manager.BackgroundTaskManager(
            parent=self,
            start_processing=True,
            max_threads=2
        )
        self._created_temp_files = []
        # set up data retriever
        self.__sg_data = sg_data.ShotgunDataRetriever(
            self,
            bg_task_manager=self._task_manager
        )
        self.__sg_data.work_completed.connect(self.__on_worker_signal)
        self.__sg_data.work_failure.connect(self.__on_worker_failure)
        self.__sg_data.start()

        # set up the UI
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.context_widget.set_up(self._task_manager)
        self.ui.context_widget.set_context(self._context)
        self.ui.context_widget.context_label.hide()
        self.ui.context_widget.restrict_entity_types_by_link("Version", "entity")

        self.ui.context_widget.context_changed.connect(self._on_context_change)
        self.ui.item_thumbnail.screen_grabbed.connect(self._update_item_thumbnail)

        self._overlay = overlay.ShotgunOverlayWidget(self)
        self.ui.submit.clicked.connect(self._submit)
        self.ui.cancel.clicked.connect(self.close)

        # set up basic UI
        self.ui.version_name.setText(self._title)

    def __del__(self):
        """
        Destructor
        """
        # clean up temp files created
        for temp_file in self._created_temp_files:
            if os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except Exception, e:
                    logger.warning(
                        "Could not remove temporary file '%s': %s" % (temp_file, e)
                    )
                else:
                    logger.debug("Removed temp file '%s'" % temp_file)

    def _format_timestamp(self, datetime_obj):
        """
        Formats the given datetime object in a short human readable form.

        :param datetime_obj: Datetime obj to format
        :returns: date str
        """
        from tank_vendor.shotgun_api3.lib.sgtimezone import LocalTimezone
        datetime_now = datetime.datetime.now(LocalTimezone())

        datetime_tomorrow = datetime_now + datetime.timedelta(hours=24)

        if datetime_obj.date() == datetime_now.date():
            # today - display timestamp - Today 01:37AM
            return datetime_obj.strftime("Today %I:%M%p")

        elif datetime_obj.date() == datetime_tomorrow.date():
            # tomorrow - display timestamp - Tomorrow 01:37AM
            return datetime_obj.strftime("Tomorrow %I:%M%p")

        else:
            # 24 June 01:37AM
            return datetime_obj.strftime("%d %b %I:%M%p")

    def closeEvent(self, event):
        """
        Executed when the dialog is closed.
        """
        try:
            self.ui.context_widget.save_recent_contexts()
            self.__sg_data.stop()
            self._task_manager.shut_down()
        except Exception:
            logger.exception("Error running Loader App closeEvent()")

        # okay to close dialog
        event.accept()

    @sgtk.LogManager.log_timing
    def _export(self, fbx_path):
        """
        Export fbx file

        :param fbx_path: temporary path where quicktime should be written
        """
        # keep track of everything currently selected. we will restore at the
        # end of the publish method
        cur_selection = cmds.ls(selection=True)

        # make sure it is selected
        cmds.select("MODEL")
        fbx_export_cmd = 'FBXExport -f "%s" -s' % (fbx_path,)
        # ...and execute it:
        try:
            self._bundle.log_debug("Executing command: %s" % fbx_export_cmd)
            mel.eval(fbx_export_cmd)
        except Exception, e:
            self._bundle.log_error("Failed to export camera: %s" % e)
            return

        # restore selection
        cmds.select(cur_selection)

    def _navigate_panel_and_close(self, panel_app, version_id):
        """
        Navigates to the given version in the given panel app
        and then closes this window.

        :param panel_app: Panel app instance to navigate.
        :prarm int version_id: Version id to navigate to
        """
        self.close()
        panel_app.navigate("Version", version_id, panel_app.PANEL)

    def _navigate_sg_and_close(self, version_id):
        """
        Navigates to the given version in shotgun and closes
        the window.

        :prarm int version_id: Version id to navigate to
        """
        self.close()
        # open sg media center playback overlay page
        url = "%s/page/media_center?type=Version&id=%d" % (
            self._bundle.sgtk.shotgun.base_url,
            version_id
        )
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(url))

    def _generate_path(self):
        template_work = self._bundle.get_template("template_work")
        template_publish = self._bundle.get_template("template_publish")
        scene_name = cmds.file(query=True, sceneName=True)
        fields = template_work.get_fields(scene_name)
        publish_path = template_publish.apply_fields(fields)
        publish_path = publish_path.replace("\\", "\\\\")
        return publish_path

    def _on_context_change(self, context):
        """
        Called when user selects a new context

        :param context: Context which was selected
        """
        logger.debug("Setting version context to %s" % context)
        self._context = context
        self._publish_path = self._generate_path()
        self._title = os.path.basename(self._publish_path)
        self.ui.version_name.setText(self._title)

    def _update_item_thumbnail(self, pixmap):
        """
        Update the version of fbx file with the given
        thumbnail pixmap
        """
        self._thumbnail = pixmap

    def _submit(self):
        """
        Submits the fbx file for review.
        """
        try:
            self._overlay.start_spin()
            self._version_id = self._run_submission()
        except Exception, e:
            logger.exception("An exception was raised.")
            self._overlay.show_error_message("An error was reported: %s" % e)

    def _upload_to_shotgun(self, shotgun, data):
        """
        Upload quicktime to Shotgun.

        :param shotgun: Shotgun API instance
        :param: parameter dictionary
        """
        logger.debug("Uploading fbx to Shotgun...")
        try:
            # shotgun.upload(
            #     "Version",
            #     data["version_id"],
            #     data["file_name"],
            #     "sg_uploaded_movie"
            # )
            self._thumbnail_path = self._get_thumbnail_as_path()
            if self._thumbnail_path:
                shotgun.upload_thumbnail(
                    "Version",
                    data["version_id"],
                    self._thumbnail_path
                )
            logger.debug("...Upload complete!")
        except Exception as e:
            logger.error(e)
        pass

    def _run_submission(self):
        """
        Carry out the fbx file and upload.
        """
        # get inputs - these come back as unicode so make sure convert to utf-8
        version_name = self.ui.version_name.text()
        if isinstance(version_name, unicode):
            version_name = version_name.encode("utf-8")

        description = self.ui.item_comments.toPlainText()
        if isinstance(description, unicode):
            description = description.encode("utf-8")

        # generate temp file for mov sequence
        fbx_path = self._generate_path()
        # ensure the publish folder exists:
        publish_folder = os.path.dirname(fbx_path)
        self._bundle.ensure_folder_exists(publish_folder)

        # and render!
        self._export(fbx_path)

        # create sg version
        data = {
            "code": version_name,
            "description": description,
            "project": self._context.project,
            "entity": self._context.entity,
            "sg_task": self._context.task,
            'sg_path_to_movie': fbx_path,
            "created_by": sgtk.util.get_current_user(self._bundle.sgtk),
            "user": sgtk.util.get_current_user(self._bundle.sgtk),
        }

        # call pre-hook
        data = self._bundle.execute_hook_method(
            "events_hook",
            "before_version_creation",
            sg_version_data=data,
            base_class=self._bundle.base_hooks.ReviewEvents
        )

        # create in shotgun
        entity = self._bundle.shotgun.create("Version", data)
        logger.debug("Version created in Shotgun %s" % entity)

        # call post hook
        self._bundle.execute_hook_method(
            "events_hook",
            "after_version_creation",
            sg_version_id=entity["id"],
            base_class=self._bundle.base_hooks.ReviewEvents
        )

        data = {"version_id": entity["id"], "file_name": fbx_path}
        self.__sg_data.execute_method(self._upload_to_shotgun, data)

        return entity["id"]

    def _get_thumbnail_as_path(self):
        """
        Helper method. Writes the associated thumbnail to a temp file
        on disk and returns the path. This path is automatically deleted
        when the object goes out of scope.

        :returns: Path to a file on disk or None if no thumbnail set
        """
        if self._thumbnail is None:
            return None

        temp_path = tempfile.NamedTemporaryFile(
            suffix=".jpg",
            prefix="sgtk_thumb",
            delete=False
        ).name
        success = self._thumbnail.save(temp_path)

        if success:
            if os.path.getsize(temp_path) > 0:
                self._created_temp_files.append(temp_path)
            else:
                logger.debug(
                    "A zero-size thumbnail was written for %s, "
                    "no thumbnail will be uploaded." % self._title
                )
                return None
            return temp_path
        else:
            logger.warning(
                "Thumbnail save to disk failed. No thumbnail will be uploaded for %s." % self._title
            )
            return None

    def __on_worker_failure(self, uid, msg):
        """
        Asynchronous callback - the worker thread errored.
        """
        self._overlay.show_error_message("An error was reported: %s" % msg)
        self.ui.submit.hide()
        self.ui.cancel.setText("Close")

    def __on_worker_signal(self, uid, request_type, data):
        """
        Signaled whenever the worker completes something.
        """

        self._bundle.execute_hook_method(
            "events_hook",
            "after_upload",
            sg_version_id=self._version_id,
            base_class=self._bundle.base_hooks.ReviewEvents
        )

        # hide spinner
        self._overlay.hide()

        # show success screen
        self.ui.stack_widget.setCurrentIndex(self.UPLOAD_COMPLETE_UI)

        # show 'jump to panel' button if we have panel loaded
        found_panel = False
        for app in self._bundle.engine.apps.values():
            if app.name == "tk-multi-shotgunpanel":
                # panel is loaded
                launch_panel_fn = lambda panel_app=app: self._navigate_panel_and_close(
                    panel_app,
                    self._version_id
                )
                self.ui.jump_to_panel.clicked.connect(launch_panel_fn)
                found_panel = True

        if not found_panel:
            # no panel, so hide button
            self.ui.jump_to_panel.hide()

        # always show 'jump to sg' button
        launch_sg_fn = lambda: self._navigate_sg_and_close(
            self._version_id
        )
        self.ui.jump_to_shotgun.clicked.connect(launch_sg_fn)

        # hide submit button, turn cancel button into a close button
        self.ui.submit.hide()
        self.ui.cancel.setText("Close")
