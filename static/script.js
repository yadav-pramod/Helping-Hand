window.onload = function() {
    getCovidStats();
    getmap();
}

function getCovidStats() {
    fetch("https://www.trackcorona.live/api/countries")
        .then(function(resp) {
            return resp.json()
        })
        .then(function(rsp) {
            rsp.data.forEach(element => {
                if (element.location == "Nepal") {

                    let recovered = element.recovered;
                    let update = element.updated;
                    let confirmedCases = element.confirmed;
                    let deaths = element.dead;

                    document.getElementById('population').innerHTML = recovered.toLocaleString('en');
                    document.getElementById('update').innerHTML = update.substr(0, 10);
                    document.getElementById('deaths').innerHTML = deaths.toLocaleString('en');
                    document.getElementById('cases').innerHTML = confirmedCases.toLocaleString('en');
                    document.getElementById('country').innerHTML = 'Nepal';
                    document.getElementById('percentage').innerHTML = ((Number(deaths) / Number(confirmedCases)) * 100).toLocaleString("en", { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + "%";

                }
            })

        })
        .catch(function() {
            console.log("AN error occured");
        })

}
setInterval(getCovidStats, 1200000);

function getmap() {
    fetch('https://www.trackcorona.live/api/countries')
        .then(function(response) {
            return response.json()
        })
        .then(function(rsp) {
            rsp.data.forEach(element => {
                latitude = element.latitude;
                longitude = element.longitude;
                cases = element.confirmed;
                var popup = new mapboxgl.Popup({

                    })
                    .setHTML(
                        "<div>" + "<h3>" + element.location + "</h3>" + "<h5>" + "Total Cases:" +
                        cases + "</h5>" + "<h5>Today Death:" + element.dead + "</h5>" + "<h5>Recovered:" + element.recovered + "</h5>" +
                        "<h5> Death Rate:" + ((100 / cases) * element.dead).toFixed(2) + "</h5>" +
                        "</div>"

                    );

                let marker = new mapboxgl.Marker({
                        draggable: false,
                        color: `rgb(${cases},0,0)`
                    })
                    .setLngLat([longitude, latitude]).addTo(map);
                marker.setPopup(popup);
                var element = marker.getElement();
                element.id = 'marker'
                element.addEventListener('mouseenter', () => popup.addTo(map));
                element.addEventListener('mouseleave', () => popup.remove());


            });
        })
}
setInterval(getmap, 1200000);


const container = document.querySelector('.data-container');
const title = document.querySelector('.title')


const tl = new TimelineMax();
tl.fromTo(container, 1, { css: { marginLeft: 0 }, css: { marginRight: 0 } }, { css: { marginLeft: "30%" }, css: { marginRight: "30%" }, ease: Power2.easeInOut })
    .fromTo(title, 0.5, { width: '50%' }, { width: '100%', ease: Power2.easeInOut });