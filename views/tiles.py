from string import Template


class Tile:
    def __init__(self, width, height, clickable):
        self._width = width
        self._height = height
        self._clickable = clickable
        self._attributes = dict()

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def clickable(self):
        return self._clickable

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
        self._attributes['class'] = self._class()
        attributes = ' '.join(['{}="{}"'.format(name, value) for (name, value) in self._attributes.items()])
        template = '<$tag $attributes><div>$content</div></$tag>'
        return Template(template).substitute(tag=self._tag(), attributes=attributes, content=self._content())

    def _content(self):
        return ""

    def _add_attribute(self, name, value):
        self._attributes[name] = value


class IconTile(Tile):
    def __init__(self, name, icon, href, color):
        super().__init__(1, 1, True)
        self.__name = name
        self.__icon = icon
        self.__href = href
        self.__color = color

    @property
    def name(self):
        return self.__name

    @property
    def icon(self):
        return "static/images/{}".format(self.__icon)

    @property
    def color(self):
        return self.__color

    @property
    def href(self):
        return self.__href

    def _class(self):
        return super()._class() + " icon"

    def _to_html(self):
        self._add_attribute('href', self.href)
        if self.color:
            self._add_attribute('style', 'background-color:{}'.format(self.color))
        return super()._to_html()

    def _content(self):
        template = '<span>$name</span><img src="$icon">'
        return Template(template).substitute(name=self.name, icon=self.icon, color=self.color)


class StatsTile(Tile):
    def __init__(self):
        super().__init__(2, 2, False)

    def _class(self):
        return super()._class() + " stats"

    def _content(self):
        return '<img src="static/images/processor.png"><br>' \
               '<img src="static/images/memory.png"><br>' \
               '<img src="static/images/memory.png"><br>' \
               '<img src="static/images/sd.png"><br>' \
               '<img src="static/images/temperature.png"><br>'


class LoginTile(Tile):
    def __init__(self):
        super().__init__(4, 1, False)

    def _class(self):
        return super()._class() + " login"

    def _content(self):
        return '<svg><polygon points="0,0 100,0 150,75 100,150 0,150"/></svg>' \
               '<img src="static/images/password.png">' \
               '<form method="post" action="login">' \
               '<input type="password" name="password" value="" placeholder="Password">' \
               '<input type="submit" name="submit" value="">' \
               '</form>'


def tiles(is_session_authenticated):
    if not is_session_authenticated:
        return [LoginTile()]
    else:
        return [IconTile(name='Logout', icon='logout.png', href='/logout', color='#C60C30'),
                StatsTile(),
                ]
