let jsonLocationData = null;

fetch("/static/location.json").then(
    response => {
        if(!response.ok){
            throw new Error("Error loading the json file");
        }
        return response.json();
    }
).then(
    data => {
        jsonLocationData = data;
    }
)

const location_content = document.getElementById("location-content");
const add_location_container = document.getElementById("add-location");

async function getLocations() {
    try {
        const response = await fetch("/config/get_locations");
        if (response.status === 200) {
            const data = await response.json();
            return data;
        } else {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
    } catch (error) {
        console.error(`Error while fetching locations : ${error}`);
        return null;
    }
}


async function displayLocation() {
    try{
        locations = await getLocations();
        locations = locations.locations;

        if (!locations || locations.length === 0) {
            location_content.innerHTML = `<p style="color: red;">No Location Set</p>`;
        } else {
            const ol = document.createElement('ol');
            for (let i = 0; i < locations.length; i++) {  // ✅ fixed typo
                const list_item = document.createElement('li');
                list_item.textContent = locations[i];
                ol.appendChild(list_item);
            }
            location_content.innerHTML = '';  // ✅ clear before adding
            location_content.appendChild(ol);
        }
    }catch (error){
        location_content.innerHTML = `<p style="color: red;">Error fetching Locations</p>`;
    }
}

function addLocationBtnPressed(){
    add_location_container.innerHTML = `
        <div>
            <label for="locationDropdown">Choose Location</label>
            <select id="locationDropdown">
                        <option value="" disabled selected></option>
            </select>
            <br>
            <button onclick = "addLocation()">Add</button>
            <br>
            <button onclick = "cancelAddingLocation()">Cancel</button>
        </div>
        `;
    const locationDropdown = document.getElementById("locationDropdown");

    jsonLocationData.locations.forEach(location => {
        option = document.createElement("option");
        option.textContent = location.displayName;
        option.value = location.displayValue;
        locationDropdown.appendChild(option);
    });
}

async function addLocation(){
    const locationDropdown = document.getElementById("locationDropdown");
    const location = locationDropdown.value;

    url = "/config/add_location";
    try{
        response = await fetch(url, {
            method : "POST",
            headers: {
                'content-type':'application/json'
            },
            body: JSON.stringify({
                "loc": location
            })
        });
        if (response.ok){
            add_location_container.innerHTML = `
            <p>${location} added successfully</p>
            <br>
            <button onclick="addLocationBtnPressed()">Add Location</button>
            `;
        }
        else{
            add_location_container.innerHTML = `
            <p>${location} was not added</p>
            <br>
            <button onclick="addLocationBtnPressed()">Add Location</button>
            `;
        }
    } catch(error){
        console.error("Network or fetch error:", error);
        add_location_container.innerHTML = `
            <p>Network or fetch error : ${error}</p>
            <br>
            <button onclick="addLocationBtnPressed()">Add Location</button>
        `;      
    }
    displayLocation();
}

function cancelAddingLocation(){
    add_location_container.innerHTML = `
        <button onclick="addLocationBtnPressed()">Add Location</button>
        `;
}

displayLocation()