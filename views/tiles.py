from string import Template


class Tile(object):
    def __init__(self, width, height, clickable):
        self.__width = width
        self.__height = height
        self.__clickable = clickable

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    @property
    def clickable(self):
        return self.__clickable

    def _class(self):
        result = "tile"
        result += " height{}".format(self.height) if self.height >= 2 else ""
        result += " width{}".format(self.width) if self.width >= 2 else ""
        return result

    def _tag(self):
        return "a" if self.clickable else "div"

    def __html__(self):
        return self._to_html()

    def _to_html(self):
        template = '<$tag class="$cls">$content</$tag>'
        return Template(template).substitute(tag=self._tag(), cls=self._class(), content=self._content())

    def _content(self):
        return ""


class IconTile(Tile):
    def __init__(self, name, icon):
        super(IconTile, self).__init__(1, 1, True)
        self.__name = name
        self.__icon = icon

    @property
    def name(self):
        return self.__name

    @property
    def icon(self):
        return "static/images/{}".format(self.__icon)

    def _class(self):
        return super(IconTile, self)._class() + " icon"

    def _content(self):
        template = '<span>$name</span><img src="$icon">'
        return Template(template).substitute(name=self.name, icon=self.icon)


class StatsTile(Tile):
    def __init__(self):
        super(StatsTile, self).__init__(1, 2, False)

    def _class(self):
        return super(StatsTile, self)._class() + " stats"

    def _content(self):
        return '<div>CPU usage:<span class=value id=cpu_value>0.0%</span></div>'+ \
               '<div class=meter><span id=cpu_percent/></div>'


class LoginTile(Tile):
    def __init__(self):
        super().__init__(2, 1, False)


class Tiles(list):
    def __init__(self, items):
        super(Tiles, self).__init__()
        self.extend(items)


tiles = Tiles(
    [
        LoginTile(),
        StatsTile(),
        IconTile(name="Torrent", icon="torrent.png"),
    ]
)