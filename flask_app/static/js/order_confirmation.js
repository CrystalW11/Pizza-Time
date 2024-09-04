function initMap() {
  const mapElement = document.getElementById("map");
  const userAddress = mapElement.getAttribute("data-address");
  const geocoder = new google.maps.Geocoder();
  const map = new google.maps.Map(mapElement, {
    zoom: 15,
    center: { lat: 0, lng: 0 },
  });

  geocoder.geocode({ address: userAddress }, function (results, status) {
    if (status === "OK") {
      map.setCenter(results[0].geometry.location);
      const marker = new google.maps.Marker({
        map: map,
        position: results[0].geometry.location,
      });
    } else {
      alert("Geocode was not successful for the following reason: " + status);
    }
  });
}

document.addEventListener("DOMContentLoaded", function () {
  initMap();
});
