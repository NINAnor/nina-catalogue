const BASE_URL = window.location.origin;

window.API_URL = `/api/v1/`;
window.PORTAL_KEY = "{{ object.uuid }}";
window.BASE_PATH = "{% url 'maps:portal-preview' slug=object.uuid %}";

window.TRANSFORM_REQUEST = (url, resourceType) => {
  if (resourceType === "Style" && url.startsWith(BASE_URL)) {
    return {
      url: url,
      credentials: "include",
    };
  }
};

window.PLAUSIBLE = null;
