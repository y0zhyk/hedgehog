showErrorMessage = function () {
    return $('span.error').fadeIn().delay(5000).fadeOut();
};

showStats = function () {
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

updateStats = function () {
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

