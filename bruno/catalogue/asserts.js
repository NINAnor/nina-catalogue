const { XMLParser, XMLBuilder } = require("fast-xml-parser");

function isValidXML(res) {
    const parser = new XMLParser();
    let jObj = parser.parse(res.getBody());

    const builder = new XMLBuilder();
    const xmlContent = builder.build(jObj);
}

function isNotAnException(res) {
    const parser = new XMLParser();
    let jObj = parser.parse(res.getBody());

    expect(jObj).not.to.have.property('ows:ExceptionReport')
}

module.exports = {
    isValidXML,
    isNotAnException,
}
