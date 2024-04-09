var cpNs=function(e){"use strict";function t(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);t&&(o=o.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,o)}return n}function n(e){for(var n=1;n<arguments.length;n++){var o=null!=arguments[n]?arguments[n]:{};n%2?t(Object(o),!0).forEach((function(t){c(e,t,o[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(o)):t(Object(o)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(o,t))}))}return e}function o(e){return o="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},o(e)}function i(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function a(e,t){for(var n=0;n<t.length;n++){var o=t[n];o.enumerable=o.enumerable||!1,o.configurable=!0,"value"in o&&(o.writable=!0),Object.defineProperty(e,s(o.key),o)}}function r(e,t,n){return t&&a(e.prototype,t),n&&a(e,n),Object.defineProperty(e,"prototype",{writable:!1}),e}function c(e,t,n){return(t=s(t))in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function s(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var n=e[Symbol.toPrimitive];if(void 0!==n){var o=n.call(e,t||"default");if("object"!=typeof o)return o;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}var l=[{id:"essential",showSwitcher:!1,content:{default:{title:"Essential",description:"Enables the site's core functionality, such as navigation, access to secure areas, video players and payments. The site cannot function properly without these cookies; they can only be disabled by changing your browser preferences."},zh:{title:"必要性",description:"启用网站核心功能，例如导航，访问安全区域，视频播放器和支付。没有这些cookie网站不能正常工作；它们仅可通过修改浏览器偏好设置禁用。"},ja:{title:"エッセンシャル",description:"移動、保護されている情報へのアクセス、動画再生、支払など、サイトの基本的な機能が有効になります。これらのクッキーが有効になっていない（お使いのブラウザの設定を変更することによってクッキーが無効化されている）場合、サイトは正しく表示されません。"}}},{id:"performance",showSwitcher:!0,content:{default:{title:"Performance",description:"Collects information on site usage, for example, which pages are most frequently visited."},zh:{title:"表现性",description:"网站使用信息收集，例如哪些网页被频繁访问。"},ja:{title:"パフォーマンス",description:"サイトの利用状況に関する情報を収集します。例として、どのページの訪問頻度が高いかのような情報です。"}}},{id:"functionality",showSwitcher:!0,content:{default:{title:"Functionality",description:"Recognises you when you return to our site. This enables us to personalise content, greet you by name, remember your preferences, and helps you share pages on social networks."},zh:{title:"功能性",description:"当你返回到我们网站时能识别您。这使得我们能个性化内容，欢迎您，记住您的偏好设置，以及帮助您分享网页到社交媒体。"},ja:{title:"機能性",description:"お客様がサイトを再訪問したときに、お客様であることを認識します。この設定では、お客様に合わせたコンテンツの表示、お客様のお名前を用いたあいさつメッセージの表示、お客様の傾向の記録を当社が行えるようになります。また、お客様がソーシャルネットワークでページをシェアできるようになります。"}}}],u={default:{notification:{title:"Your tracker settings",body1:"We use cookies and similar methods to recognise visitors and remember preferences. We also use them to measure campaign effectiveness and analyse site traffic.",body2:"By selecting ‘Accept‘, you consent to the use of these methods by us and trusted third parties.",body3:'For further details or to change your consent choices at any time see our <a href="https://ubuntu.com/legal/data-privacy?cp=hide#cookies">cookie policy</a>.',buttonAccept:"Accept all and visit site",buttonManage:"Manage your tracker settings"},manager:{title:"Tracking choices",body1:"We use cookies to recognise visitors and remember your preferences.",body2:"They enhance user experience, personalise content and ads, provide social media features, measure campaign effectiveness, and analyse site traffic.",body3:"Select the types of trackers you consent to, both by us, and third parties.",body4:'Learn more at <a href="https://ubuntu.com/legal/data-privacy?cp=hide#cookies">data privacy: cookie policy</a> - you can change your choices at any time from the footer of the site.',acceptAll:"Accept all",acceptAllHelp:'This will switch all toggles "ON".',SavePreferences:"Save preferences"}},zh:{notification:{title:"您的追踪器设置",body1:"我们使用cookie和相似的方法来识别访问者和记住偏好设置。我们也用它们来衡量活动的效果和网站流量分析。",body2:"选择”接受“，您同意我们和受信的第三方来使用这些方式。",body3:'更多内容或者随时地变更您的同意选择，请点击我们的 <a href="https://ubuntu.com/legal/data-privacy?cp=hide#cookies">cookie策略</a>.',buttonAccept:"接受全部和访问网站",buttonManage:"管理您的追踪器设置"},manager:{title:"追踪选项",body1:"我们使用cookie来识别访问者和记住您的偏好设置",body2:"它们增强用户体验，使内容和广告个性化，提供社交媒体功能，衡量活动效果和网站流量分析。",body3:"选择您同意授予我们和受信的第三方的追踪类型。",body4:'点击<a href="https://ubuntu.com/legal/data-privacy?cp=hide#cookies">数据隐私：cookie策略</a>了解更多，您可以在网站底部随时更改您的选择。',acceptAll:"接受全部",acceptAllHelp:"这将把全部开关变为”开启“。",SavePreferences:"保存偏好设置"}},ja:{notification:{title:"トラッキング機能の設定",body1:"当社は、当社のウェブサイトを訪問された方の識別や傾向の記録を行うために、クッキーおよび類似の手法を利用します。また、キャンペーンの効果の測定やサイトのトラフィックの分析にもクッキーを利用します。",body2:"「同意」を選択すると、当社および信頼できる第三者による上記の手法の利用に同意したものとみなされます。",body3:'詳細または同意の変更については、いつでも当社の<a href="https://ubuntu.com/legal/data-privacy?cp=hide#cookies">クッキーに関するポリシー</a>をご覧になることができます。',buttonAccept:"すべて同意してサイトにアクセス",buttonManage:"トラッキング機能の設定の管理"},manager:{title:"トラッキング機能の選択",body1:"当社は、当社のウェブサイトを訪問された方の識別や傾向の記録を行うために、クッキーを利用します。",body2:"クッキーは、お客様の利便性の向上、お客様に合わせたコンテンツや広告の表示、ソーシャルメディア機能の提供、キャンペーンの効果の測定、サイトのトラフィックの分析に役立ちます。",body3:"当社および第三者によるトラッキング機能のタイプから、お客様が同意されるものをお選びください。",body4:'詳細は、<a href="https://ubuntu.com/legal/data-privacy?cp=hide#cookies">データプライバシー：クッキーに関するポリシー</a>をご覧ください。お客様が選んだ設定は、本サイトの下部からいつでも変更できます。',acceptAll:"すべて同意",acceptAllHelp:"同意されるとすべての設定が「ON」に切り替わります。",SavePreferences:"設定を保存"}}},d={ad_storage:"denied",ad_user_data:"denied",ad_personalization:"denied",analytics_storage:"denied",functionality_storage:"denied",personalization_storage:"denied",security_storage:"denied"},p=["security_storage"],f=["ad_storage","ad_user_data","ad_personalization","analytics_storage"],h=["functionality_storage","personalization_storage"],y=["ad_storage","ad_user_data","ad_personalization","analytics_storage","functionality_storage","personalization_storage"],b=function(e){var t=new Date;t.setTime(t.getTime()+31536e6);var n="expires="+t.toUTCString();document.cookie="_cookies_accepted="+e+"; "+n+"; samesite=lax;path=/;",E(e)&&O()},g=function(){for(var e="_cookies_accepted=",t=document.cookie.split(";"),n="",o="",i=0;i<t.length;i++){for(var a=t[i];" "==a.charAt(0);)a=a.substring(1);o=a.substring(e.length,a.length),0===a.indexOf(e)&&"true"!==o&&(n=o)}return n},m=function(){var e=g();return!e||"true"==e},v=function(){return"hide"===new URLSearchParams(window.location.search).get("cp")},k=function(e){return u[e]?u[e]:u.default},w=function(e,t){return e.content[t]?e.content[t]:e.content.default},_=function(){var e=g();e&&S(e)},S=function(e){var t=j(d,e);L(t)},j=function(e,t){var o=n({},e);return p.forEach((function(e){o[e]="granted"})),"performance"===t?f.forEach((function(e){o[e]="granted"})):"functionality"===t?h.forEach((function(e){o[e]="granted"})):"all"===t&&y.forEach((function(e){o[e]="granted"})),o},L=function(e){window.gtag("consent","update",e)},O=function(){"object"===("undefined"==typeof dataLayer?"undefined":o(dataLayer))&&dataLayer.push({event:"pageview"})},E=function(e){return"all"==e||"performance"==e},P=function(){function e(t,n,o){i(this,e),this.container=t,this.renderManager=n,this.destroyComponent=o}return r(e,[{key:"getNotificationMarkup",value:function(e){var t=k(e);return'\n      <div class="p-modal" id="modal">\n        <div class="p-modal__dialog" role="dialog" aria-labelledby="cookie-policy-title" aria-describedby="cookie-policy-content">\n        <header class="p-modal__header">\n          <h2 class="p-modal__title" id="cookie-policy-title">'.concat(t.notification.title,'</h2>\n        </header>\n        <div id="cookie-policy-content">\n          <p>').concat(t.notification.body1,"</p>\n          <p>").concat(t.notification.body2,"</p>\n          <p>").concat(t.notification.body3,'</p>\n          <p class="u-no-margin--bottom">\n            <button class="p-button--positive js-close" id="cookie-policy-button-accept">').concat(t.notification.buttonAccept,'</button>\n            <button class="p-button js-manage">').concat(t.notification.buttonManage,"</button>\n          </p>\n        </div>\n      </div>")}},{key:"render",value:function(e){this.container.innerHTML=this.getNotificationMarkup(e),this.initaliseListeners()}},{key:"initaliseListeners",value:function(){var e=this;this.container.querySelector(".js-close").addEventListener("click",(function(t){b("all"),S("all"),e.destroyComponent()})),this.container.querySelector(".js-manage").addEventListener("click",(function(t){e.renderManager()}))}}]),e}(),A=function(){function e(t,n,o){i(this,e),this.language=o,this.id=t.id,this.title=w(t,o).title,this.description=w(t,o).description,this.showSwitcher=t.showSwitcher,this.container=n,this.element,this.render()}return r(e,[{key:"render",value:function(){var e=this.cookieIsTrue(),t=document.createElement("div");t.classList.add("u-sv3"),t.innerHTML="\n      ".concat(this.showSwitcher?'<label class="u-float-right p-switch">\n        <input type="checkbox" class="p-switch__input js-'.concat(this.id,'-switch" ').concat(e&&'checked=""','>\n        <span class="p-switch__slider"></span>\n      </label>'):"","\n      <h4>").concat(this.title,"</h4>\n      <p>").concat(this.description,"</p>"),this.container.appendChild(t),this.element=t.querySelector(".js-".concat(this.id,"-switch"))}},{key:"cookieIsTrue",value:function(){var e=g();return!(!e||e!==this.id&&"all"!==e)||e&&e===this.id}},{key:"isChecked",value:function(){return!!this.element&&this.element.checked}},{key:"getId",value:function(){return this.id}}]),e}(),M=function(){function e(t,n){i(this,e),this.container=t,this.controlsStore=[],this.destroyComponent=n}return r(e,[{key:"getManagerMarkup",value:function(e){var t=k(e).manager;return'\n    <div class="p-modal" id="modal">\n    <div class="p-modal__dialog" role="dialog" aria-labelledby="modal-title" aria-describedby="modal-description">\n      <header class="p-modal__header">\n        <h2 class="p-modal__title" id="modal-title">'.concat(t.title,'</h2>\n      </header>\n      <p id="modal-description">').concat(t.body1,"</p>\n      <p>").concat(t.body2,"</p>\n      <p>").concat(t.body3,"</p>\n      <p>").concat(t.body4,'</p>\n      <p><button class="p-button--positive u-no-margin--bottom js-close">').concat(t.acceptAll,"</button></p>\n      <p>").concat(t.acceptAllHelp,'</p>\n      <hr />\n      <div class="controls"></div>\n      <button class="p-button js-save-preferences">').concat(t.SavePreferences,"</button>\n    </div>\n  </div>")}},{key:"render",value:function(e){var t=this;this.container.innerHTML=this.getManagerMarkup(e);var n=this.container.querySelector(".controls");l.forEach((function(o){var i=new A(o,n,e);t.controlsStore.push(i)})),this.initaliseListeners()}},{key:"initaliseListeners",value:function(){var e=this;this.container.querySelector(".js-close").addEventListener("click",(function(){b("all"),S("all"),e.destroyComponent()})),this.container.querySelector(".js-save-preferences").addEventListener("click",(function(){e.savePreferences(),e.destroyComponent()}))}},{key:"savePreferences",value:function(){var e=this.controlsStore.filter((function(e){return e.isChecked()}));this.controlsStore.length===e.length?b("all"):this.controlsStore.forEach((function(e){e.isChecked()&&b(e.getId())})),function(e){var t=e.filter((function(e){return e.isChecked()})),o=n({},d);t.forEach((function(e){o=j(o,e.id)})),L(o)}(this.controlsStore)}}]),e}();window.gtag||(window.dataLayer=window.dataLayer||[],window.gtag=function(){dataLayer.push(arguments)},window.gtag("consent","default",d));return e.cookiePolicy=function(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:null,t=null,n=document.documentElement.lang,o=function(e){(e&&e.preventDefault(),null===t)&&((t=document.createElement("dialog")).classList.add("cookie-policy"),t.setAttribute("open",!0),document.body.appendChild(t),new P(t,i,a).render(n),document.getElementById("cookie-policy-button-accept").focus())},i=function(){new M(t,a).render(n)},a=function(){"function"==typeof e&&e(),document.body.removeChild(t),t=null},r=function(){_();var e=document.querySelector(".js-revoke-cookie-manager");e&&e.addEventListener("click",o),m()&&!v()&&o()};document.addEventListener("DOMContentLoaded",r,!1)},e}({});
//# sourceMappingURL=cookie-policy.js.map
