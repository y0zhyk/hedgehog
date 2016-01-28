from string import Template


class Tile:
    def __init__(self, width, height):
        self.__width = width
        self.__height = height
        self._content = None

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    def _update_content(self):
        pass

    @property
    def __content(self):
        self._update_content()
        return self._content.to_html() if self._content is not None else ""

    @property
    def __class(self):
        cls = ['tile']
        if self.height >= 2:
            cls.append('height{}'.format(self.height))
        if self.width >= 2:
            cls.append('width{}'.format(self.width))
        return ' '.join(cls)

    def __html__(self):
        template = '<div class="$cls">$content</div>'
        return Template(template).substitute(cls=self.__class, content=self.__content)


class TileContent:
    def __init__(self, tag='div'):
        self.__tag = tag
        self.__attributes = dict()
        self.__content = ''

    def add_attribute(self, name, value):
        self.__attributes[name] = value

    @property
    def tag(self):
        return self.__tag

    def to_html(self):
        attributes = ' '.join(['{}="{}"'.format(name, value) for (name, value) in self.__attributes.items()])
        template = '<$tag $attributes>$content</$tag>'
        return Template(template).substitute(tag=self.__tag, attributes=attributes, content=self.__content)

    def set_content(self, content):
        self.__content = content


class ClickableTile(Tile):
    def __init__(self, width, height, href):
        super().__init__(width, height)
        self.__href = href
        self._content = TileContent('a')

    @property
    def href(self):
        return self.__href

    def _update_content(self):
        self._content.add_attribute('href', self.href)


class ClickableIconTile(ClickableTile):
    def __init__(self, name, icon, href, color=None):
        super().__init__(1, 1, href)
        self.__icon = icon
        self.__color = color
        self.__name = name

    @property
    def icon(self):
        return "static/images/{}".format(self.__icon)

    @property
    def color(self):
        return self.__color

    @property
    def name(self):
        return self.__name

    def _update_content(self):
        super()._update_content()
        self._content.add_attribute('class', 'icon')
        if self.color:
            self._content.add_attribute('style', 'background-color:{}'.format(self.color))
        template = '<span>$name</span><img src="$icon">'
        content = Template(template).substitute(name=self.name, icon=self.icon, color=self.color)
        self._content.set_content(content)


class StatsTile(Tile):
    def __init__(self):
        super().__init__(2, 2)
        self._content = TileContent()

    def _update_content(self):
        self._content.add_attribute('class', 'stats')
        content = '<script>$(document).ready(function() { return showStats(); }); </script>'
        self._content.set_content(content)


class LoginTile(Tile):
    CONTEXT = \
        '''
        <svg><polygon points="0,0 100,0 150,75 100,150 0,150"/></svg>
        <img src="static/images/password.png">
        <script>
            $(document).ready(function() {
                $.ajax({
                    url: "/api/login",
                    success: function(response){
                        $("div.login").append(response);
                        $(".login > span").delay(5000).fadeOut();
                    }
                });
            });
        </script>
        '''

    def __init__(self):
        super().__init__(4, 1)
        self._content = TileContent()

    def _update_content(self):
        self._content.add_attribute('class', 'login')
        self._content.set_content(self.CONTEXT)


def tiles(is_session_authenticated):
    if not is_session_authenticated:
        return [LoginTile()]
    else:
        return [StatsTile(),
                ClickableIconTile(name='Logout', icon='logout.png', href='/api/logout', color='#C60C30'),
                ClickableIconTile(name='Wifi', icon='wifi.png', href='http://hedgehog.no-ip.info', color='#1E7145'),
                ]
