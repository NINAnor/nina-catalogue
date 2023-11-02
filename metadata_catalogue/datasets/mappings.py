# based on https://github.com/geopython/pycsw/blob/master/pycsw/core/config.py
MD_CORE_MODEL = {
    "typename": "gmd:MD_Metadata",
    "outputschema": "http://www.isotc211.org/2005/gmd",
    "mappings": {
        "pycsw:Identifier": "identifier",
        "pycsw:Typename": "csw_typename",
        "pycsw:Schema": "csw_schema",
        "pycsw:MdSource": "csw_mdsource",
        "pycsw:InsertDate": "csw_insert_date",
        "pycsw:XML": "metadata_xml",
        "pycsw:AnyText": "csw_anytext",
        "pycsw:Language": "language",
        "pycsw:Title": "title",
        "pycsw:Abstract": "abstract",
        "pycsw:Keywords": "keywords",
        "pycsw:KeywordType": "empty",
        "pycsw:Format": "empty",
        "pycsw:Source": "empty",
        "pycsw:Date": "empty",
        "pycsw:Modified": "empty",
        "pycsw:Type": "empty",
        "pycsw:BoundingBox": "csw_wkt_geometry",
        "pycsw:CRS": "empty",
        "pycsw:AlternateTitle": "empty",
        "pycsw:RevisionDate": "empty",
        "pycsw:CreationDate": "empty",
        "pycsw:PublicationDate": "empty",
        "pycsw:Organization": "empty",
        "pycsw:OrganizationName": "empty",
        "pycsw:SecurityConstraints": "empty",
        "pycsw:ParentIdentifier": "empty",
        "pycsw:TopicCategory": "empty",
        "pycsw:ResourceLanguage": "empty",
        "pycsw:GeographicDescriptionCode": "empty",
        "pycsw:Denominator": "empty",
        "pycsw:DistanceValue": "empty",
        "pycsw:DistanceUOM": "empty",
        "pycsw:TempExtent_begin": "empty",
        "pycsw:TempExtent_end": "empty",
        "pycsw:ServiceType": "empty",
        "pycsw:ServiceTypeVersion": "empty",
        "pycsw:Operation": "empty",
        "pycsw:CouplingType": "empty",
        "pycsw:OperatesOn": "empty",
        "pycsw:OperatesOnIdentifier": "empty",
        "pycsw:OperatesOnName": "empty",
        "pycsw:Degree": "empty",
        "pycsw:AccessConstraints": "empty",
        "pycsw:OtherConstraints": "empty",
        "pycsw:Classification": "empty",
        "pycsw:ConditionApplyingToAccessAndUse": "empty",
        "pycsw:Lineage": "empty",
        "pycsw:ResponsiblePartyRole": "empty",
        "pycsw:SpecificationTitle": "empty",
        "pycsw:SpecificationDate": "empty",
        "pycsw:SpecificationDateType": "empty",
        "pycsw:Creator": "creator",
        "pycsw:Publisher": "publisher",
        "pycsw:Contributor": "contributor",
        "pycsw:Relation": "empty",
        "pycsw:Links": "empty",
    },
}
