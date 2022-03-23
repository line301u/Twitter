
////////////////////////////////
// HANDLE EVENTS
function openEditTweet(event){
    let targetTweet = event.target.closest("form").nextElementSibling;
    targetTweet.classList.remove("hide");
}
function closeEditTweet(event){
    let targetTweet = event.target.closest(".edit_tweet_container");
    targetTweet.classList.add("hide");
}


////////////////////////////////
// POST TWEET
async function tweet(){
    const form = event.target.form;

    // CREATE REQUEST
    const connection = await fetch("/tweet", {
        method : "POST",
        body : new FormData(form)
    });

    // REQUEST FAILED
    if(!connection.ok){
        alert("could not tweet")
        return;
    };

    // SUCESS
    let tweet = await connection.json();

    // CREATE TWEET ELEMENT
    let section_tweet = `
    <div class="tweet">
    <form class="tweet-${tweet.tweet_id}" onsubmit="return false">
        <input name="tweet_id" type="hidden" value="${tweet.tweet_id}">
        <span>${tweet.tweet_created_at}</span>
        ${tweet.tweet_updated_at ? 
        `<span class="tweet_updated_at">Last edited: ${tweet.tweet_updated_at}</span>` 
        : ''}
        ${!tweet.tweet_updated_at ? 
            `<span class="tweet_updated_at hide">Last edited: ${tweet.tweet_updated_at}</span>` 
            : ''}
        <p class="tweet_text">${tweet.tweet_text}</p>
        ${tweet.tweet_image_path && tweet.tweet_image_path !== 'null' ? 
            `<img class="tweet_image" src="../images/${tweet.tweet_image_path}" alt="Tweet image">` 
            : ''}
        <div class="button-wrapper">
            <button onclick="openEditTweet(event)" class="edit-tweet-button white-button" type="button">Edit</button>
            <button class="white-button" onclick="deleteTweet(event)">Delete tweet</button>
        </div>
    </form>

<div class="edit_tweet_container hide">
    <div class="edit_tweet">
        <form onsubmit="return false">
            <input name="tweet_id" type="hidden" value="${tweet.tweet_id}">
            <label>Tweet text</label>
            <input name="tweet_text" type="text" value="${tweet.tweet_text}">
            ${tweet.tweet_image_path ? 
                `<label>Change picture</label>` 
                : '<label>Upload a picture</label>'}
            <input name="tweet_image_path" type="hidden" value="${tweet.tweet_image_path}">
            <input type="file" id="tweet_image" name="tweet_image" value="${tweet.tweet_id}">
            <div class="button-wrapper">
                <span onclick="closeEditTweet(event)" class="cancel-edit">Cancel</span>
                <button onclick="updateTweet(event)" class="blue-button">Save</button>
            </div>
        </form>
    </div>
</div>
</div>
    `
    // INSERT TWEET ELEMENT IN DOM
    document.querySelector(".tweets_container").insertAdjacentHTML("afterbegin", section_tweet);

    // CLEAR IMPUT FIELDS
    form.querySelector(".tweet_text").value = null;
    form.querySelector("#tweet_image").value = null;
}

////////////////////////////////
// UPDATE TWEET
async function updateTweet(event){
    const form = event.target.form;
    const tweet_id = form.querySelector("input[name='tweet_id']").value;

    // CREATE REQUEST
    const connection = await fetch(`/update-tweet/${tweet_id}`, {
        method : "PUT",
        body : new FormData(form)
    });

    // REQUEST FAILED
    if(!connection.ok){
        alert("could not tweet")
        return;
    };

    // SUCESS
    const updated_tweet = await connection.json();

    // DEFINE ELEMENTS TO MANIPULATE DOM
    const edited_tweet_element = document.querySelector(`.tweet-${tweet_id}`)
    const tweet_image_element = form.querySelector("input[name='tweet_image_path']");

    var timestamp = updated_tweet.tweet_updated_at;

    // CONVERT TWEET_UDPATED_AT (EPOCH) TO DATETIME
    let converted_epoch = covertEpochToDateTime(timestamp);

    edited_tweet_element.querySelector(".tweet_updated_at").innerHTML = converted_epoch;
    edited_tweet_element.querySelector(".tweet_updated_at").classList.remove("hide")
    edited_tweet_element.querySelector(".tweet_text").innerHTML = updated_tweet.tweet_text;

    // DEFINE IF TWEET INCLUDES AN IMAGE BEFORE UPDATE
    let doesTweetInculdeImage = true;
    if (tweet_image_element.value === "null" || tweet_image_element.value === "None" || tweet_image_element.value === undefined) {doesTweetInculdeImage = false}

    // DEFINE IF UPDATED TWEET INCLUDES AN IMAGE
    let doesUpdatedTweetInculdeImage = true;
    if (updated_tweet.tweet_image_path === "null" || updated_tweet.tweet_image_path === "None" || tweet_image_element.value === undefined) {
        doesUpdatedTweetInculdeImage = false
    }

    // ADD IMAGETAG TO DOM IF NOT ALREADY IMAGE IN TWEET    
    if (!doesTweetInculdeImage && doesUpdatedTweetInculdeImage){
        const new_image_element = `<img class="tweet_image" src="../images/${updated_tweet.tweet_image_path}" alt="Tweet image"></img>`
        edited_tweet_element.querySelector(".tweet_text").insertAdjacentHTML("afterend", new_image_element);
        tweet_image_element.value = updated_tweet.tweet_image_path;
    }

    // CHANGE IMAGE IN TWEET
    if (doesTweetInculdeImage && doesUpdatedTweetInculdeImage){
        edited_tweet_element.querySelector("img").src = `../images/${updated_tweet.tweet_image_path}`;
        tweet_image_element.value = updated_tweet.tweet_image_path;
    }

    closeEditTweet(event)
}

////////////////////////////////
// DELETE TWEET
async function deleteTweet(event){
    const form = event.target.form;
    const tweet_id = form.querySelector("input[name='tweet_id']").value;

    // CREATE REQUEST
    const connection = await fetch(`/delete-tweet/${tweet_id}`, {
        method : "DELETE",
    });

    // CREATE FAILED
    if(!connection.ok){
        alert("could not delete tweet")
        return;
    };

    // SUCESS
    const response = await connection.text();

    form.remove();
}

////////////////////////////////
// CONVERT EPOCH TO DATETIME
function covertEpochToDateTime(timestamp){
    let date = new Date(timestamp * 1000);
    let year = date.getFullYear();
    let month = ('0' + (date.getMonth() + 1)).slice(-2);
    let day = date.getDate();
    let hours = date.getHours();
    let ampm = hours >= 12 ? 'PM' : 'AM';
    let minutes = date.getMinutes();

    return `Last edited: ${hours}:${minutes} ${ampm}, ${day}-${month}-${year}`;
}