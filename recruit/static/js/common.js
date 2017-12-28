var DANAL = window.DANAL || {};

DANAL.AJAXCall = function(url, data, fn){
    console.log(data);
  var resultData = {};
  $.ajax({
      url:url,
      type: "POST",
      data: data,
      error: function(){
          resultData = {
              "data":{
                  "RETURNCODE":"-1",
                  "RETURNMSG":"내부 오류가 발생했습니다. 관리자에게 문의해주세요."
              }
          };
          if(fn){
              fn(resultData);
          }
      },
      success: function(result){
          resultData = result;
          if(fn){
              fn(resultData);
          }
      }
  }).done(function(){
  });
  return resultData;
};

DANAL.getURLVars = (function() {
    var vars = [], hash;
    var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
    for(var i = 0; i < hashes.length; i++){
        hash = hashes[i].split('=');
        vars.push(hash[0]);
        vars[hash[0]] = hash[1];
    }
    return vars;
})

DANAL.checkForm = function(form, alert_elem, chkFlag, pwd){
    var patterns = {};
    patterns["PASSWORD"] = /^(((?=.*[a-z])(?=.*\d))|((?=.*[a-z])(?=.*[^a-z\s\d]))|((?=.*\d)(?=.*[^a-z\s\d]))).{8,15}$/;
    patterns["EMPTY"] = /[^ ].+/;
    patterns["EMAIL"] = /((\w+[\w\.]*)@(\w+[\w\.]*)\.([A-Za-z]+))/;
    patterns["PHONE"] = /\d{10,11}/;
    patterns["NUMBER"] = /\d+/;

    if(chkFlag === "CHECKBOX"){
        if(form.prop("checked")){
            alert_elem.hide();
            return true;
        }else{
            alert_elem.show();
            return false;
        }
        //체크박스 form 검증

    }else if(chkFlag === "PWD_CONFIRM"){
        if(form.val() === pwd.val()){
            alert_elem.hide();
            return true;
        }else{
            alert_elem.show();
            return false;
        }
        //비밀번호 일치 검증
    }else{
        if(patterns[chkFlag].test(form.val())){
            if(typeof(alert_elem) !== "string"){
                alert_elem.hide();
            }
            return true;
        }else{
            if(typeof(alert_elem) !== "string"){
                alert_elem.show();
            }else{
                alert(alert_elem);
            }
            return false;
            // 오류 안내 elem없이 단순 alert인 경우
        }
        // 정규식을 이용한 form 검증
    }



}


DANAL.EnterKeyEvent = (function(){
    var init = function(login_btn){
        $("input").keydown(function (e) {
            if(e.which === 13){
                login_btn.trigger("click");
            }
        });
    }

    return {
        init:init
    }
}() );