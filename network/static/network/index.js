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

closeNewPost.addEventListener("click", () => {
    postPopUp.style.display = "block";
    newPostDiv.style.display = "none";
    overlay.style.display = "none";
})

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