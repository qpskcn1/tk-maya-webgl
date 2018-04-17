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
        self._title = "test"

        self._task_manager = task_manager.BackgroundTaskManager(
            parent=self,
            start_processing=True,
            max_threads=2
        )

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

        self._overlay = overlay.ShotgunOverlayWidget(self)
        self.ui.submit.clicked.connect(self._submit)
        self.ui.cancel.clicked.connect(self.close)

        # set up basic UI
        self.ui.version_name.setText(self._title)

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
    def _render(self, mov_path, start_frame, end_frame):
        """
        Export fbx file

        :param mov_path: temporary path where quicktime should be written
        :param int start_frame: First frame to render
        :param int end_frame: Last frame to render
        """
        pass

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

    def _on_context_change(self, context):
        """
        Called when user selects a new context

        :param context: Context which was selected
        """
        logger.debug("Setting version context to %s" % context)
        self._context = context
        self._title = self._generate_title()
        self.ui.version_name.setText(self._title)

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
        logger.debug("Uploading movie to Shotgun...")
        try:
            shotgun.upload(
                "Version",
                data["version_id"],
                data["file_name"],
                "sg_uploaded_movie"
            )
            logger.debug("...Upload complete!")
        finally:
            sgtk.util.filesystem.safe_delete_file(data["file_name"])

    def _run_submission(self):
        """
        Carry out the fbx file and upload.
        """
        # get inputs - these come back as unicode so make sure convert to utf-8
        version_name = self.ui.version_name.text()
        if isinstance(version_name, unicode):
            version_name = version_name.encode("utf-8")

        description = self.ui.description.toPlainText()
        if isinstance(description, unicode):
            description = description.encode("utf-8")

        # set metadata
        self._setup_formatting(version_name)

        # generate temp file for mov sequence
        mov_path = os.path.join(tempfile.gettempdir(), "quickreview.mov")
        mov_path = sgtk.util.filesystem.get_unused_path(mov_path)

        # and render!
        self._render(mov_path, start_frame, end_frame)

        # create sg version
        data = {
            "code": version_name,
            "description": description,
            "project": self._context.project,
            "entity": self._context.entity,
            "sg_task": self._context.task,
            "created_by": sgtk.util.get_current_user(self._bundle.sgtk),
            "user": sgtk.util.get_current_user(self._bundle.sgtk),
            "sg_first_frame": start_frame,
            "sg_last_frame": end_frame,
            "frame_count": end_frame - start_frame + 1,
            "frame_range": "%d-%d" % (start_frame, end_frame),
            "sg_movie_has_slate": True
        }

        if self.ui.playlists.itemData(self.ui.playlists.currentIndex()) != 0:
            data["playlists"] = [{
                "type": "Playlist",
                "id": self.ui.playlists.itemData(self.ui.playlists.currentIndex())
            }]

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

        data = {"version_id": entity["id"], "file_name": mov_path}
        self.__sg_data.execute_method(self._upload_to_shotgun, data)

        return entity["id"]

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
