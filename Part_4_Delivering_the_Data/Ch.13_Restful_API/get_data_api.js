let data

async function init() {
    data = await getData('winners/?category=Physics&country=United States')
    console.log(`${data.length} US Physics winners:`, data)
    // send the data to a suitable charting function
    //drawChart(data)
}

init()

async function getData(ep='winners/?category=Physics'){
    let API_URL = "https://deployment-flask-api.ew.r.appspot.com/"
    let response = await fetch(API_URL + ep)
    
    let data = response.json()

    return data
}