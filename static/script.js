function showPDF(file) {
  var w = $( document ).width() - 300;
  var h = $( window ).height() - $('p#head').height();
  $("#result").animate({
                width: "300px",
                height: h
              });
  $("#result").css('background', '#ccc');

  $("#detail").attr('tag', file)
  $("#detail").css('width', w);
  $("#docview").css('height', h);

  $("#cmd").html('<a href="'+file+'/Apdf.pdf" target="_blank">Download PDF</a>&nbsp;<a href="'+file+'" target="_blank">Ordner &ouml;ffnen</a>');
  var pdf = new PDFObject({
    url: file + "/Apdf.pdf",
    pdfOpenParams: {
      view: "FitH"
    }
  }).embed("docview");
}

  $(function() {
    var submit_form = function(e) {
      $('#result').css('float', 'none');
      $('#result').html("<img src='/static/loader.png'>");
      $('#result').css('width', 'auto');
      $.get('/q/', {
        q: $('input[name="q"]').val()
        }, function(data) {
          $('p#head').animate({ margin: 0 }, 500, function() {
            $('#result').css('float', 'left');
            $('#result').html(data);
            $('#detail').html("<span id='cmd'></span><div id='docview'></div>");
            document.title = $('input[name="q"]').val()
            $('h1#title').text($('input[name="q"]').val())

            $('a.doc').click(function(){
              showPDF($(this).attr('tag'));
            });
 
            if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|BB|PlayBook|IEMobile|Windows Phone|Kindle|Silk|Opera Mini/i.test(navigator.userAgent)) {
              $('#result').css('margin', 0);
              $('a.doc').css('margin', 0);
              $('a.doc img').css('width', '106px');
              $('a.doc img').css('height', '150px');
            } else {
              $('input[name=q]').focus().select();
            }
          });
      });
      return false;
    };

    // Search form
    $('a#go').bind('click', submit_form);
    $('input[type=text]').bind('keydown', function(e) {
      if (e.keyCode == 13) {
        submit_form(e);
      }
    });
    $('input[name=q]').val();
    $('input[name=q]').focus();

    // Current state
    $("#state").load('/state');
    setInterval(function() {
       $("#state").load('/state');
      }, 3000);
  });
