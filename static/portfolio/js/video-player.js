// Видео плеер обязан быть единственным на странице
let videoPlayer = document.getElementById('video-player');
let sourceList = videoPlayer.querySelectorAll('source');

function playVideo(pk) {
    openVideoPlayer();
    changeVideo(pk);
}

function changeVideo(pk) {
    for (let source of sourceList) source.src = '/stream_video/' + pk + '/';
    videoPlayer.load(); // нужно для перезагрузки видео с новым источником
}

function openVideoPlayer() {
    let div = document.querySelector('.video-player');
    div.style.display = 'block';
}

function closeVideoPlayer() {
    let div = document.querySelector('.video-player');
    div.style.display = 'none';
}