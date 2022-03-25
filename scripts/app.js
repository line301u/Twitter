
////////////////////////////////
// HANDLE EVENTS
function openEditTweet(){
    let targetTweet = event.target.form;
    const edit_tweet_form = document.querySelector(".edit_tweet_container")
    edit_tweet_form.classList.remove("hide");

    target_tweet = {
        "tweet_id" : targetTweet.querySelector("input[name='tweet_id']").value,
        "tweet_text" : targetTweet.querySelector(".tweet_text").innerHTML,
        "tweet_image_path" : targetTweet.querySelector("input[name='tweet_image_path']").value
    }

    // CREATE UPDATE TWEET ELEMENT
    edit_tweet_form.querySelector("input[name='tweet_text']").value = target_tweet["tweet_text"];
    edit_tweet_form.querySelector("input[name='tweet_id']").value = target_tweet["tweet_id"];
    edit_tweet_form.querySelector("input[name='tweet_image_path']").value = "";
    edit_tweet_form.querySelector(".tweet_image_tag").src = ""

    // CHECK IF TWEET INCLUDES AN IMAGE
    if (target_tweet["tweet_image_path"] && target_tweet["tweet_image_path"] !== "None" && target_tweet["tweet_image_path"] !== "null") {
        edit_tweet_form.querySelector(".tweet_image_tag").src = `/images/${target_tweet["tweet_image_path"]}`
        edit_tweet_form.querySelector("input[name='tweet_image_path']").value = target_tweet["tweet_image_path"];
        edit_tweet_form.querySelector(".tweet_image_tag").classList.remove("hide")
        edit_tweet_form.querySelector(".edit-tweet-file-uplad").textContent = "Do you want to change the image?"
    } else {
        edit_tweet_form.querySelector(".edit-tweet-file-uplad").textContent = "Do you want to add an image?"
    }
}

function closeEditTweet(event){
    let edit_tweet_container = document.querySelector(".edit_tweet_container");
    edit_tweet_container.classList.add("hide");
    edit_tweet_container.querySelector(".tweet_image_tag").classList.add("hide")
}

////////////////////////////////
// POST TWEET
async function tweet(event){
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
            <input name="tweet_image_path" type="hidden" value="${tweet.tweet_image_path}">
            ${tweet.tweet_image_path && tweet.tweet_image_path !== 'null' ? 
                `<img class="tweet_image" src="../images/${tweet.tweet_image_path}" alt="Tweet image">` 
                : ''}
            <div class="button-wrapper">
                <button onclick="openEditTweet(event)" class="edit-tweet-button white-button" type="button">Edit</button>
                <button class="white-button" onclick="deleteTweet(event)">Delete tweet</button>
            </div>
        </form>
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

    // CONVERT TWEET_UDPATED_AT (EPOCH) TO DATETIME
    let timestamp = updated_tweet.tweet_updated_at;
    let converted_epoch = covertEpochToDateTime(timestamp);

    edited_tweet_element.querySelector(".tweet_updated_at").innerHTML = converted_epoch;
    edited_tweet_element.querySelector(".tweet_updated_at").classList.remove("hide")
    edited_tweet_element.querySelector(".tweet_text").innerHTML = updated_tweet.tweet_text;

    // DEFINE IF TWEET INCLUDES AN IMAGE BEFORE UPDATE
    let doesTweetInculdeImage = true;
    if (!tweet_image_element.value || tweet_image_element.value === "null" || tweet_image_element.value === "None" || tweet_image_element.value === undefined) {doesTweetInculdeImage = false}
    
    // DEFINE IF UPDATED TWEET INCLUDES AN IMAGE
    let doesUpdatedTweetInculdeImage = true;
    if (!updated_tweet.tweet_image_path || updated_tweet.tweet_image_path === "null" || updated_tweet.tweet_image_path === "None" || tweet_image_element.value === undefined) {
        doesUpdatedTweetInculdeImage = false
    }

    // ADD IMAGETAG TO DOM IF NOT ALREADY IMAGE IN TWEET    
    if (!doesTweetInculdeImage && doesUpdatedTweetInculdeImage){
        const new_image_element = `<img class="tweet_image" src="../images/${updated_tweet.tweet_image_path}" alt="Tweet image"></img>`
        edited_tweet_element.querySelector("input[name='tweet_image_path']").value = updated_tweet.tweet_image_path;
        edited_tweet_element.querySelector(".tweet_text").insertAdjacentHTML("afterend", new_image_element);
        tweet_image_element.value = updated_tweet.tweet_image_path;
    }

    // CHANGE IMAGE IN TWEET
    if (doesTweetInculdeImage && doesUpdatedTweetInculdeImage){
        edited_tweet_element.querySelector("input[name='tweet_image_path']").value = updated_tweet.tweet_image_path;
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