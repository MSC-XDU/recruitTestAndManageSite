$(
    $("button#check").click(function () {
        var value = $("input").val();
        window.location = "/admin/search?s="+value
    })
);
$(
    $('#department').on('change',function(){
    var selectValue = $("#department option:selected").val();
    var info = {department:selectValue};
    var r = $.ajax({
      url: "/admin/department",
      type: "post",
      async: false,
      data: info,
      dataType: "html"
    });
    if (r.status == 200){
      $('.resultList').remove();
      $(".main").append(r.responseText)
        }
    })
)