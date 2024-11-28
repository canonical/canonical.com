var downloadLinks = document.querySelectorAll('.js-download');
var os = 'linux';

if (navigator.appVersion.indexOf('Win') != -1) { os = 'win-win' };
if (navigator.appVersion.indexOf('MacOS') != -1) { os = 'mac' };
if (navigator.appVersion.indexOf('Mac OS') != -1) { os = 'mac' };
if (navigator.appVersion.indexOf('Macintosh') != -1) { os = 'mac' };

for (var i = 0; i < downloadLinks.length; i++) {
  if (downloadLinks[i].dataset.os === os) {
    downloadLinks[i].classList.add('p-button--positive');
  }
}

