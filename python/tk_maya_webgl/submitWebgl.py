import os
import pymel.core as pm
import maya.cmds as cmds
import maya.mel as mel

from .dialog import SubmitWebGLDialog

class webglPublishManager(object):

    def __init__(self, app, context=None):
        """
        Construction
        """
        self._app = app
        self.sg = self._app.sgtk.shotgun
        self._context = context if context else self._app.context
        template_work = self._app.get_template("template_work")
        template_publish = self._app.get_template("template_publish")
        scene_name = pm.sceneName()
        fields = template_work.get_fields(scene_name)
        self.fbx_publish_path = template_publish.apply_fields(fields)
        self.fbx_publish_path = self.fbx_publish_path.replace("\\", "\\\\")

    def show_dialog(self):
        try:
            self._app.engine.show_dialog("Model Review %s" % self._app.version,
                                         self._app, SubmitWebGLDialog, self._app, self)
        except Exception as e:
            self._app.log_error(e)

    def publish(self):
        # keep track of everything currently selected. we will restore at the
        # end of the publish method
        cur_selection = cmds.ls(selection=True)

        # ensure the publish folder exists:
        publish_folder = os.path.dirname(self.fbx_publish_path)
        self._app.ensure_folder_exists(publish_folder)

        # make sure it is selected
        cmds.select("MODEL")
        fbx_export_cmd = 'FBXExport -f "%s" -s' % (self.fbx_publish_path,)
        # ...and execute it:
        try:
            self._app.log_debug("Executing command: %s" % fbx_export_cmd)
            mel.eval(fbx_export_cmd)
        except Exception, e:
            self._app.log_error("Failed to export camera: %s" % e)
            return
        data = {'project': self._context.project,
                'code': os.path.basename(self.fbx_publish_path),
                'description': "WebGL Online Review",
                'sg_path_to_movie': self.fbx_publish_path,
                'entity': self._context.entity,
                'sg_task': self._context.task,
                }

        self._create_version(data)

        # restore selection
        cmds.select(cur_selection)

    def _create_version(self, data):

        result = None
        try:
            filters = [["project", "is", data["project"]],
                       ["code", "is", data["code"]],
                       ]
            # check if a version entity with same code exists in shotgun
            # if none, create a new version Entity with fbx name as its code
            version = self.sg.find_one("Version", filters)
            if version:
                self._app.log_debug("Version already exist, updating")
                result = self.sg.update('Version', version["id"], data)
            else:
                self._app.log_debug("Create a new Version as %s" % data["code"])
                result = self.sg.create('Version', data)
                self._upload_to_shotgun(result['id'])
        except Exception as e:
            self._app.log_error("Cannot create/update the version \n%s" % e)
        return result

    def _upload_to_shotgun(self, version_id):
        try:
            self._app.log_debug("Uploading fbx to Shotgun: %s" %
                                self.fbx_publish_path)
            result = self.sg.upload("Version", version_id,
                                    self.fbx_publish_path,
                                    field_name="sg_uploaded_movie")
            self._app.log_debug("Uploaded! % s" % result)
            return result
        except Exception as e:
            self._app.log_error("Cannot upload to shotgun \n %s" % e)
