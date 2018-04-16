# Copyright (c) 2013 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.

"""
An app that syncs the frame range between a scene and a shot in Shotgun.

"""
import tank
import traceback


class BaseWebGLSetup(tank.platform.Application):

    WebglPublishManager = None

    def init_app(self):
        """
        Called as the application is being initialized
        """
        self.engine.register_command("Submit WebGL Review", self.run_app)

    def destroy_app(self):
        """
        App teardown
        """
        self.log_debug("Destroying tk-maya-webgl app")

    def run_app(self):
        """
        Start doing Webgl Publish
        """
        try:
            WebglPublishManager = self.get_webglpublish_manager()
            WebglPublishManager.publish()
        except:
            traceback.print_exc()

    def get_webglpublish_manager(self):
        """
        Create a singleton WebglPublishManager object to be used by any app.
        """
        if self.WebglPublishManager is None:
            tk_maya_webgl = self.import_module("tk_maya_webgl")
            self.WebglPublishManager = tk_maya_webgl.webglPublishManager(self)
        return self.WebglPublishManager
