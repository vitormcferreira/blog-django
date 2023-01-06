function increment(element, value = 1) {
  element.innerHTML = Number(element.innerHTML) + value;
}

function handleLike(likeId, dislikeId, url, csrf) {
  const likeBtn = document.querySelector(likeId);
  const like = document.querySelector(likeId + ' span');
  const dislikeBtn = document.querySelector(dislikeId);
  const dislike = document.querySelector(dislikeId + ' span');

  handleClick(url, csrf, (res) => {
    if (res.status === 201) {
      // se o usuário está caom dislike marcado
      if (dislikeBtn.classList.contains('active')) {
        // desmarca dislike
        increment(dislike, -1);
        dislikeBtn.classList.remove('active')
      }
      // se o usuário está com like marcado
      if (likeBtn.classList.contains('active')) {
        // desmarca o like
        increment(like, -1);
        likeBtn.classList.remove('active');
      } else {
        // marca o like
        increment(like);
        likeBtn.classList.add('active');
      }
    }
  });
}

function handleDislike(likeId, dislikeId, url, csrf) {
  const likeBtn = document.querySelector(likeId);
  const like = document.querySelector(likeId + ' span');
  const dislikeBtn = document.querySelector(dislikeId);
  const dislike = document.querySelector(dislikeId + ' span');

  handleClick(url, csrf, (res) => {
    if (res.status === 201) {
      if (likeBtn.classList.contains('active')) {
        increment(like, -1);
        likeBtn.classList.remove('active');
      }
      if (dislikeBtn.classList.contains('active')) {
        increment(dislike, -1);
        dislikeBtn.classList.remove('active');
      } else {
        increment(dislike);
        dislikeBtn.classList.add('active');
      }
    }
  });
}

function handleClick(url, csrf, callback) {
  fetch(url, { method: 'POST', headers: { 'X-CSRFToken': csrf } }).then(callback);
}
