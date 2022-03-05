import KeithleySeries2400InteractiveSmu_Constants as _smuconst


class DisplayConfiguration:
    def __init__(self):
        self._mycomms = None
        self.input = self.Input()

    def update_comms(self):
        """
        This function is used to ensure lower level consumer classes tied to the driver are updated to promote \
        instrument communications.

        :return:
        """
        self.input._mycomms = self._mycomms

    def change_screen(self, screen_name):
        """
        This function changes which front-panel screen is displayed.

        :param screen_name: DISPLAY_SCREEN_MAIN, DISPLAY_SCREEN_GRAPH, DISPLAY_SCREEN_GRAPH_SWIPE,
        DISPLAY_SCREEN_HISTOGRAM, DISPLAY_SCREEN_HOME_LARGE_READING, DISPLAY_SCREEN_PROCESSING,
        DISPLAY_SCREEN_READING_TABLE, DISPLAY_SCREEN_SETTINGS_SWIPE, DISPLAY_SCREEN_SOURCE_SWIPE,
        DISPLAY_SCREEN_STATS_SWIPE
        :return:
        """
        screen_string = ""
        if screen_name is _smuconst.DISPLAY_SCREEN_HOME:
            screen_string = "display.SCREEN_HOME"
        elif screen_name is _smuconst.DISPLAY_SCREEN_GRAPH:
            screen_string = "display.SCREEN_GRAPH"
        elif screen_name is _smuconst.DISPLAY_SCREEN_GRAPH_SWIPE:
            screen_string = "display.SCREEN_GRAPH_SWIPE"
        elif screen_name is _smuconst.DISPLAY_SCREEN_HISTOGRAM:
            screen_string = "display.SCREEN_HISTOGRAM"
        elif screen_name is _smuconst.DISPLAY_SCREEN_HOME_LARGE_READING:
            screen_string = "display.SCREEN_HOME_LARGE_READING"
        elif screen_name is _smuconst.DISPLAY_SCREEN_PROCESSING:
            screen_string = "display.SCREEN_PROCESSING"
        elif screen_name is _smuconst.DISPLAY_SCREEN_READING_TABLE:
            screen_string = "display.SCREEN_READING_TABLE"
        elif screen_name is _smuconst.DISPLAY_SCREEN_SETTINGS_SWIPE:
            screen_string = "display.SCREEN_SETTINGS_SWIPE"
        elif screen_name is _smuconst.DISPLAY_SCREEN_SOURCE_SWIPE:
            screen_string = "display.SCREEN_SOURCE_SWIPE"
        elif screen_name is _smuconst.DISPLAY_SCREEN_STATS_SWIPE:
            screen_string = "display.SCREEN_STATS_SWIPE"
        elif screen_name is _smuconst.DISPLAY_SCREEN_USER_SWIPE:
            screen_string = "display.SCREEN_USER_SWIPE"

        self._mycomms.write(f"display.changescreen({screen_string})")

    class Input:
        def __init__(self):
            self._mycomms = None
