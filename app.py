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
        self.tk_maya_webgl = self.import_module("tk_maya_webgl")
        self._base_hooks = self.tk_maya_webgl.base_hooks
        self.engine.register_command("Model Review", self.create_review)

    @property
    def base_hooks(self):
        """
        Exposes the ``base_hooks`` module.

        This module provides base class implementations hooks.

        Access to these classes won't typically be needed when writing hooks as
        they are are injected into the class hierarchy automatically for any
        collector or publish plugins configured.

        :return: A handle on the app's ``base_hooks`` module.
        """
        return self._base_hooks

    def destroy_app(self):
        """
        App teardown
        """
        self.log_debug("Destroying tk-maya-webgl app")

    @property
    def context_change_allowed(self):
        """
        Specifies that context changes are allowed.
        """
        return True

    def create_review(self):
        """
        Called from the gizmo when the review button is pressed.

        :param group_node: The nuke node that was clicked.
        """
        self.engine.show_dialog(
            "Model Review",
            self,
            self.tk_maya_webgl.Dialog
        )
