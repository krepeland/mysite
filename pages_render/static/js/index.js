async function callClick(){
  let response = await fetch('/click/',{
    method: 'GET'
  });
  let answer = await response.json();
  document.getElementById("data").innerHTML = answer.coinsCount;
  console.log(answer.boosts);
  if(answer.boosts){
    renderBoosts(answer.boosts);
  }
}

let boosts_names = ["Smol beaver", "Beaver", "Big beaver", "Axebeaver", "Chains-Z-Z-Z-saw", "Log manipulator",
                    "Scientist", "Druid", "Meditator", "Cultist", "THE BEAVER"
                   ]
async function getUser(id){
  let response = await fetch('/users/' + id,{
    method: 'GET'
  });
  let answer = await response.json();

  document.getElementById("user").innerHTML = answer['username'];
  let getCycle = await fetch('/cycles/' + answer['cycle'],{
    method: 'GET'
  });
  let cycle = await getCycle.json();
  document.getElementById("data").innerHTML = cycle['coinsCount'];

  call_boost_render();
}

function buyBoost(boost_id) {

    const csrftoken = getCookie('csrftoken')

    fetch('/buyBoost/', {
        method: 'POST',
        headers: {
            "X-CSRFToken": csrftoken,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            boost_id: boost_id
        })
    }).then(response => {
        if (response.ok) {
            return response.json()
        } else {
            return Promise.reject(response)
        }
    }).then(data => {
        document.getElementById("data").innerHTML = data['coinsCount'];
        document.getElementById("clickPower").innerHTML = data['clickPower'];
        call_boost_render()
    })

}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== ''){
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

async function call_boost_render(){
    let boost_request = await fetch('/boosts/', {
        method :'GET'
    })
    let boosts = await boost_request.json();
    renderBoosts(boosts);
}

function renderBoosts(boosts){
    let parent = document.getElementById("boosts-list")
    parent.innerHTML =''
    boosts.reverse();
    boosts.forEach(boost => {
        addBoost(parent, boost)
    })
}

function addBoost(parent, boost){
    const boostHolder = document.createElement('li')
    boostHolder.setAttribute('class', 'boosts-list-item')
    if (+document.getElementById("data").innerHTML < boost.price)
        boostHolder.setAttribute('class', 'boosts-list-item disabled');

    boostHolder.innerHTML = `
    <span>
        <div class="boost-name"><strong>${boosts_names[(boost.boost_id) % boosts_names.length]}</strong></div>
        <div class="boost-level">Count: <span id="boostLevel">${boost.level}</span></div>
        <div class="boost-price">Cost: <span id="boostPrice">${boost.price}</span></div>
        <div class="boost-power">Power: <span id="boostPower">${boost.power}</span></div>
    </span>
    <input type="image" class="clickable boost boost_${boost.boost_id}" src="https://psv4.userapi.com/c534536/u190403673/docs/d34/bf8ed4b458a2/alpha.png?extra=lI_8Bs3huO5aSxZbjNJInsHh3JQ1GRAx7MMDnKova3tc8rsKGvWpqHR8jSJwBMmFYhUfqJjx4pe0TodyXpesvyCTzfedhzNWfZe5nrEfyzs9Nz3YVHMV5P8SKQRn--ayi4_cEu4269IANUgfL_mpy_3-" onclick="buyBoost(${boost.boost_id})" />
    `

    parent.appendChild(boostHolder)
}
