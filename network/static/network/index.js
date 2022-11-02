const popUpBottom = document.querySelector("#post-popup-button");
const postPopUp = document.querySelector("#post-popup");
const newPostDiv = document.querySelector("#new-post");
const overlay =  document.getElementById("overlay");
const closeNewPost =  document.getElementById("close-new-post");
const postContent = document.querySelector("#post-content")

if ( popUpBottom ) {
    popUpBottom.addEventListener("click", () => {
        postPopUp.style.display = "none";
        newPostDiv.style.display = "block";
        overlay.style.display = "block";
    });
    
    overlay.addEventListener("click", (e) => {
        if ( overlay !== e.target ) return;
        
        postPopUp.style.display = "block";
        newPostDiv.style.display = "none";
        overlay.style.display = "none";
    });
}

if ( closeNewPost ) {
  closeNewPost.addEventListener("click", () => {
    postPopUp.style.display = "block";
    newPostDiv.style.display = "none";
    overlay.style.display = "none";
  })
}

if (postContent) {
  postContent.addEventListener("input", () => {
    postContent.style.height = `200px`
    if (postContent.scrollHeight > 200) {
        if (postContent.scrollHeight > 650) {
            postContent.style.height = "650px"
            return
        } 
        postContent.style.height = `${postContent.scrollHeight + 2}px`
        console.log(postContent.scrollHeight)
    }
  })
}


function editPost(postId) {
    const post = document.querySelector(`#post-${postId}`)
    content = post.querySelector("h5")
    post.innerHTML = `
    <form id=form-${postId} action="{% url 'posts' %}" method="post">
        <div class="form-group">
            <textarea autofocus class="form-control" type="text" name="body">${content.innerText}</textarea>
        </div>
        <div class="form-group">
            <input class="btn btn-primary" type="submit">
        </div>
    </form>
    `
    let form = document.querySelector(`#form-${postId}`)
    form.addEventListener("submit", function(event) {
        // Stop the default submit event action
        event.preventDefault();
        url = window.location.href
        const formData = new FormData(this);
        fetch(`/posts`, {
          method: "PUT",
          body: JSON.stringify({
            body: formData.get('body'),
            id: postId
          })
        })
        .then(() => {
            location.reload();
          })
        .catch(function (err) { console.log(err)}) 
      });
}

async function liked(postId) {
    const post = document.querySelector(`#post-${postId}`);
    let likeCounter = document.querySelector(`#like-${postId}`)
    let button = document.querySelector(`#likes-${postId}`);
    res = await likePost(postId, likeCounter)
    if (button.value == "Like") { button.value = "Unlike";}
    else {button.value = "Like";}
}

async function likePost(postId, likeCounter) {
  await fetch(`/likes`, {
    method: "POST",
    body: JSON.stringify({
      post_id: postId
    })
  })
  .then(() => {
    fetch(`/posts?post=${postId}`)
    .then((res) => {
      return res.json()
    })
    .then((data) => {
      likeCounter.innerText = data.likes + " Likes"
    })
    return true
  })
  .catch(function (err) { 
    console.log(err)
    return false
  })
};