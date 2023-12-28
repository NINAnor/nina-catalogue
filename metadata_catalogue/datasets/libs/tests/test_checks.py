import pytest

from ...models import Dataset
from ..checks import vrt


@pytest.mark.django_db(transaction=True)
def test_vrt_validation():
    d = Dataset.objects.create(name="test")
    c = d.get_content()
    c.gdal_vrt_definition = """
<OGRVRTDataSource>
    <OGRVRTLayer name="my_table">
        <SrcDataSource>IGNORE</SrcDataSource>
        <SrcLayer>IGNORE</SrcLayer>
        <GeometryType>wkbPoint</GeometryType>

        <FieldDefn name="id"    type="Integer" />
        <FieldDefn name="name"  type="String" />
        <FieldDefn name="value" type="Real" />

        <Feature>
            <Field name="id">1</Field>
            <Field name="name">John</Field>
            <Field name="value">42.5</Field>
            <Geometry>
                <Point>
                    <Coordinates>1.0,2.0</Coordinates>
                </Point>
            </Geometry>
        </Feature>

        <Feature>
            <Field name="id">2</Field>
            <Field name="name">Jane</Field>
            <Field name="value">63.2</Field>
            <Geometry>
                <Point>
                    <Coordinates>3.0,4.0</Coordinates>
                </Point>
            </Geometry>
        </Feature>

        <!-- Add more Feature blocks for additional rows -->

    </OGRVRTLayer>
</OGRVRTDataSource>
    """
    c.save()
    vrt()
