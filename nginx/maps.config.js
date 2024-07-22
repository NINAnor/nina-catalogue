const BASE_URL = window.location.origin

window.API_URL = `/api/v1/`;
window.PORTAL_KEY = "34005d2a-5d57-470b-98d9-9ed119a265b9"

window.TRANSFORM_REQUEST = (url, resourceType) => {
    if (resourceType === 'Style' && url.startsWith(BASE_URL)) {
        return {
            url: url,
            credentials: 'include',
        }
    }
}

window.PLAUSIBLE = null;
