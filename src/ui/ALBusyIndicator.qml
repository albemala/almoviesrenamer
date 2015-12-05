import QtQuick 2.5

Row {
    id: layout
    width: itemWidth * itemsCount + itemsSpacing * (itemsCount - 1)
    height: 27
    spacing: itemsSpacing

    property int itemWidth: 4
    property int itemsCount: 9
    property int itemsSpacing: 3

    Repeater {
        model: itemsCount

        Rectangle {
            id: item
            width: itemWidth
            height: layout.height
            transform: scaleTransform
            color: "darkGray"
            property int itemIndex: index
            property Scale scaleTransform: Scale {
                yScale: 0.2
                origin.y: layout.height / 2
            }

            SequentialAnimation {
                id: animation
                running: true

                property int duration: 300

                NumberAnimation {
                    duration: animation.duration * item.itemIndex
                }
                SequentialAnimation {
                    loops: Animation.Infinite

                    NumberAnimation {
                        target: scaleTransform
                        property: "yScale"
                        to: 1.0
                        duration: 100
                    }
                    NumberAnimation {
                        target: scaleTransform
                        property: "yScale"
                        to: 0.2
                        easing.type: Easing.OutCubic
                        duration: 700
                    }
                    NumberAnimation {
                        duration: animation.duration * layout.itemsCount
                    }
                }
            }
        }
    }
}

