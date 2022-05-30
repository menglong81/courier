/**
 * Created by menglong.zhou on 2019/6/30.
 */
$.form_prompt_modify = function(text, title, html, onOK, onCancel) {
    var config;
    if (typeof text === 'object') {
      config = text;
    } else {
      config = {
        text: text,
        title: title,
        onOK: onOK,
        onCancel: onCancel,
        html: html
      }
    }

    var modal = $.modal({
      text: '<p class="weui-prompt-text">'+(config.text || '')+'</p>' + config.html,

      title: config.title,
      autoClose: false,
      buttons: [
      {
        text:'取消',
        className: "default",
        onClick: function () {
          $.closeModal();
          config.onCancel && config.onCancel.call(modal);
        }
      }, {
        text: '确定',
        className: "primary",
        onClick: function() {
          if(config.autoClose){
            $.closeModal();
          }
          config.onOK && config.onOK.call(modal);
        }
      }]
    });
    return modal;
  };