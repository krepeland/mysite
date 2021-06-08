async function callClick(){
  const coins_counter = document.getElementById('data')
  let coins_value = parseInt(coins_counter.innerText)
  const click_power = document.getElementById('clickPower').innerText
  coins_value += parseInt(click_power)
  document.getElementById("data").innerHTML = coins_value
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

  set_auto_click()
  set_send_coins_interval()
  call_boost_render(answer.cycle);
}

function buyBoost(boost_id) {
    send_coins()

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
        console.log(data);
        document.getElementById("data").innerHTML = data['coinsCount'];
        document.getElementById("clickPower").innerHTML = data['clickPower'];
        document.getElementById("auto_click_power").innerHTML = data['auto_click_power'];
        renderBoosts(data['boosts'])
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

async function call_boost_render(cycle){
    let boost_request = await fetch('/boosts/' + cycle, {
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
    if(boost.boost_id >= boosts_names.length)
        return
    const boostHolder = document.createElement('li')

    boost_auto = ""
    boost_type = "Power"
    if (boost.boost_id % 3 == 0){
        boost_auto = "boosts-list-item-auto"
        boost_type = "Power/S"
    }

    boostHolder.setAttribute('class', 'boosts-list-item ' + boost_auto)
    if (+document.getElementById("data").innerHTML < boost.price)
        boostHolder.setAttribute('class', 'boosts-list-item disabled');


    boostHolder.innerHTML = `
    <span>
        <div class="boost-name"><strong>${boosts_names[(boost.boost_id) % boosts_names.length]}</strong></div>
        <div class="boost-level">Count: <span id="boostLevel">${boost.level}</span></div>
        <div class="boost-price">Cost: <span id="boostPrice">${boost.price}</span></div>
        <div class="boost-power">${boost_type}: <span id="boostPower">${boost.power}</span></div>
    </span>
    <input type="image" class="clickable boost boost_${boost.boost_id}" src="https://psv4.userapi.com/c534536/u190403673/docs/d34/cae4a6091479/alpha.png?extra=Yi6Jk0T5Tjn9BFVbDoxBC7nXsIo3MyrBVUe6qIWLHTBE0_FDuDmy8G2_5kcUnBrQ45TxDy4eWlS6nct_vsBCtYwrKl_2MPckAlra7HK4kwfAkpYsuRlJ5F1OTAOJ1_Y_mCwO8MNuN7ULjF9ns4xRQqmK" onclick="buyBoost(${boost.boost_id})" />
    `

    parent.appendChild(boostHolder)
}

function set_auto_click() {
    setInterval(function() {
        const coins_counter = document.getElementById('data')
        let coins_value = parseInt(coins_counter.innerText)

        const auto_click_power = document.getElementById('auto_click_power').innerText
        coins_value += parseInt(auto_click_power)
        document.getElementById("data").innerHTML = coins_value;
    }, 1000)
}

function set_send_coins_interval() {
    setInterval(function() { send_coins() }, 2000)
}

function send_coins() {
        const csrftoken = getCookie('csrftoken')
        const coins_counter = document.getElementById('data').innerText
        console.log(coins_counter)
        fetch('/set_main_cycle/', {
            method: 'POST',
            headers: {
                "X-CSRFToken": csrftoken,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                coinsCount: coins_counter,
            })
        }).then(response => {
            if (response.ok) {
                return response.json()
            } else {
                return Promise.reject(response)
            }
        }).then(data => {
            console.log(data)
            if (data.boosts)
              renderBoosts(data.boosts)
            document.getElementById("auto_click_power").innerHTML = data['auto_click_power'];
        }).catch(err => console.log(err))
}