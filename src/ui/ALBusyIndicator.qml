import QtQuick 2.5

Row {
    id: layout
    width: itemWidth * itemsCount + 3 * 9
    spacing: 3

    property int itemWidth: 4
    property int itemsCount: 10

    Repeater {
        model: itemsCount
        Rectangle {
            width: itemWidth
            height: layout.height
            color: "darkGray"
        }
    }
}

