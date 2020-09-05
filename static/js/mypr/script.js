$.fn.thumbnail = function(baseURL){
    var serverURL = "http://capture.heartrails.com/320x240/round/border/shadow?";
    return this.each(function(){
        $(this).hover(
            function(e){
                var url = $(this).attr("href");
                $("#jqThumbnail").attr("src",serverURL+url);
                $("#jqThumbnail").css("left",e.pageX-150);
                $("#jqThumbnail").css("top",e.pageY+30);
                $("#jqThumbnail").show();
            },
            function(){
                $("#jqThumbnail").hide();
            }
        );
    });
}
$(function(){
    $("body").append("<img src='' id='jqThumbnail' width='320' height='240' style='position:absolute;display:none'>");
    $("a.thumb").thumbnail();

    // #で始まるリンクをクリックしたら実行
    $('a[href^="#"]').click(function() {
        var speed = 400;
        var href= $(this).attr("href");
        var target = $(href == "#" || href == "" ? 'html' : href);
        var position = target.offset().top;
        $('body,html').animate({scrollTop:position}, speed, 'swing');
        return false;
    });

    // クリックされたらcheckedを外す
    $('#nav-content li a').on('click', function(event) {
        $('#nav-input').prop('checked', false);
    });
});