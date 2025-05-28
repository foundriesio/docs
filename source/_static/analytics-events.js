/**
 * The name of the analytics event property in the data-* attributes.
 */
const datasetEventProperty = "analyticsEvent";

/**
 * List of properties set in the data-* attributes of the element
 * that will be passed into the eventInfo object.
 */
const datasetEntries = [
  ["analyticsAction", "action"],
  ["analyticsDetail", "detail"],
  ["analyticsLabel", "label"],
  ["analyticsLocation", "location"],
];

const datasetProperties = new Map(datasetEntries);
Object.freeze(datasetProperties);

function handleAnalyticsEvent({ event, eventInfo }) {
  window.adobeDataLayer = window.adobeDataLayer || [];
  window.adobeDataLayer.push({
    event,
    eventInfo,
  });
}

document.addEventListener("click", function (event) {
  const { target } = event;

  let element = target;
  // eslint-disable-next-line security/detect-object-injection
  if (element.dataset[datasetEventProperty]) {
    element = target;
  } else {
    element = target.closest("[data-analytics-event]");
  }

  if (element) {
    const { dataset } = element;

    const eventInfo = {};
    for (const [property, analyticsValue] of datasetProperties) {
      if (Object.hasOwn(dataset, property)) {
        // eslint-disable-next-line security/detect-object-injection
        eventInfo[analyticsValue] = dataset[property];
      }
    }

    handleAnalyticsEvent({
      // eslint-disable-next-line security/detect-object-injection
      event: dataset[datasetEventProperty],
      eventInfo,
    });
  }
});
