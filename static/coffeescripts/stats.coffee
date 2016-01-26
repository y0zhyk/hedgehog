$(document).ready ->
  showStats()

showStats = () ->
  $.getJSON 'api/stats', (data) ->
    for stat in data.stats
      $("div.stats").append "<div class=stat id=#{stat.id}><img src=/static/images/#{stat.id}.png><div class=value/><div class=meter><span/></div></div>"
    updateStats()

updateStats = () ->
  $.getJSON 'api/stats', (data) ->
    for stat in data.stats
      $("##{stat.id} .value").text stat.value
      $("##{stat.id} span").width "#{stat.percent}%"
    $("#time").text data.time
    setTimeout updateStats, 10000
