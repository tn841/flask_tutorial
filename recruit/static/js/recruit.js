"use strict";

var DANAL = window.DANAL || {}; //패키지화
DANAL.recruit = window.DANAL.recruit || {};

DANAL.recruit.ClickUIEvent = (function(){
    var login = (function(){
        var init = function(){
            $("#email, #pwd").focusout(function(){
                var email = $(this).attr("id");
                var pattern;
                if(/email/.test(email)){
                    pattern="EMAIL";
                }else{
                    $(this).val().replace(""," ");
                    pattern = "EMPTY"
                }
                DANAL.checkForm($(this), $(this).next(), pattern)
            });
        };

        return {
            init: init
        }
    }() );

    var register = (function(){
        var init = function(){
            //가입 폼 체크
            $("#name, #email, #pwd, #pwd_confirm").focusout(function(){
                var id = $(this).attr("id");
                var pattern;
                if(/name/.test(id)){
                    pattern="EMPTY";
                }else if(/email/.test(id)){
                    pattern="EMAIL";
                }else if(/pwd/.test(id)){
                    pattern="PASSWORD";
                }else if(/pwd_confirm/.test(id)){
                    pattern="PWD_CONFIRM";
                }else{
                    $(this).val().replace("", " ");
                    pattern="EMPTY";
                }
                DANAL.checkForm($(this), $(this).next(), pattern);
            });

            //비밀번호 확인 체크
            $("#pwd_confirm").focusout(function(){

                if($("#pwd_confirm").val() !== $("#pwd").val()){
                    $(this).next().show();
                }else{
                    $(this).next().hide();
                }

            });
        };

        return {
            init: init
        };
    }() );

    return {
        login: login,
        register: register
    }
}() );