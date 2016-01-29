var showStats = function () {
    return $.getJSON('api/stats', function (data) {
        var i, len, ref, stat;
        ref = data.stats;
        for (i = 0, len = ref.length; i < len; i++) {
            stat = ref[i];
            $("div.stats").append("<div class=stat id=" + stat.id + "><img src=/static/images/" + stat.id + ".png><div class=value/><div class=meter><span/></div></div>");
        }
        return updateStats();
    });
};

var updateStats = function () {
    return $.getJSON('api/stats', function (data) {
        var i, len, ref, stat;
        ref = data.stats;
        for (i = 0, len = ref.length; i < len; i++) {
            stat = ref[i];
            $("#" + stat.id + " .value").text(stat.value);
            $("#" + stat.id + " span").width(stat.percent + "%");
        }
        $("#time").text(data.time);
        return setTimeout(updateStats, 10000);
    });
};

$(document).ready(function () {

    var Consts = {
        tileSize: 150,
        gutter: 10
    };

    var Tile = function () {
        this.width = 0;
        this.height = 0;
        this.self = 0;
    };

    var tiles = [];

    //var maxNumberOfTiles = Math.floor(windowWidth / (Consts.tileSize + Consts.gutter))

    var totalTilesWidth = 0;
    var maxTileHeight = 0;
    $('.tile').each(function () {
        var tile = new Tile();
        tile.width = this.offsetWidth;
        tile.height = this.offsetHeight;
        tile.self = this;
        totalTilesWidth += tile.width + Consts.gutter;
        maxTileHeight = Math.max(tile.height, maxTileHeight);
        tiles.push(tile);
    });

    var rearrange = function () {
        var windowWidth = $('body').width();
        if (totalTilesWidth <= windowWidth) {
            var x = Math.floor((windowWidth - totalTilesWidth) / 2);
            var numberOfTiles = tiles.length;
            for (var i = 0; i < numberOfTiles; i++) {
                var tile = tiles[i];
                $(tile.self).css({
                    left: x
                });
                x += tile.width + Consts.gutter;
            }

            $('footer').css({
                top: 100 + maxTileHeight + Consts.gutter
            });

        }

    };

    $(window).resize(function () {
        rearrange();
    });

    rearrange();

});