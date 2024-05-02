var dagcomponentfuncs = (window.dashAgGridComponentFunctions = window.dashAgGridComponentFunctions || {});

dagcomponentfuncs.DMC_ActionIcon = function (props) {
    const {setData, data, rowIndex} = props;

    function onClick() {
        setData({
            rowIndex: rowIndex,
            drugName: data.drug_name,
            dateApproval: data['Date of Approval']
        });
    }

    const iconElement = React.createElement(window.dash_iconify.DashIconify, {
        icon: props.icon,
        color: props.iconColor,
        width: props.iconWidth,
        height: props.iconHeight
    });

    return React.createElement(
        window.dash_mantine_components.ActionIcon,
        {
            onClick: onClick,
            variant: props.variant,
            style: {
                margin: props.margin,
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                marginTop: props.marginTop,
                marginLeft: props.marginLeft,
            }
        },
        iconElement
    );
};
