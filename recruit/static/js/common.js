$(function(){

})

var AJAXCall = function(url, data, fn){
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


function getUrlVars()
{
    var vars = [], hash;
    var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
    for(var i = 0; i < hashes.length; i++)
    {
        hash = hashes[i].split('=');
        vars.push(hash[0]);
        vars[hash[0]] = hash[1];
    }
    return vars;
}