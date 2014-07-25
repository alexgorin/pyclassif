
Ext.onReady(function() {
    var panel = Ext.create('Ext.panel.Panel', {
        width : window.innerWidth,
        height: window.innerHeight,
        id: 'mainPanel',
        layout : 'border',
        items : [
            northPanel,
            centralPanel,
            southPanel,
        ]
    });
    panel.render(Ext.getBody());

    handler = ( function() {
        panel.setHeight(window.innerHeight);
        panel.setWidth(window.innerWidth);
    });

    window.onresize = handler;
})
