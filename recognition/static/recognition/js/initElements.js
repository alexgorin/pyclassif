Ext.Loader.setConfig({
        enabled	: true,
        paths	: {
            Ext : "{% static 'extjs' %}",
            "Ext.ux": "{% static 'extjs/examples/ux' %}",
        }
    });
    
Ext.require("*");

var northPanel = Ext.create('Ext.panel.Panel', {
    id: 'northPanel',
    //height: "10%",
    region: 'north',
    items: [{
        xtype : 'panel',
        region: 'center'
    }]
});

var centralPanel = Ext.create('Ext.panel.Panel', {
    id: 'centralPanel',
    region: 'center',
    layout: 'border',
    height: "80%",
    split: true,
    tbar: [
            {text:'Page1', handler: function() {}},
            '-',
            {text:'Page2', handler: function() {}},
            '-',
    ],
    items: [{
        xtype : 'textfield',
        id: 'emptyField',
        region: 'center',
        layout: 'border',
    }]
});

var southPanel = Ext.create('Ext.panel.Panel', {
    id: 'southPanel',
    region: 'south',
    layout: 'border',
    height: "5%",
    split: true,
    items: [{
        xtype : 'label',
        region: 'center',
        text: 'Developed by alexgorin (saniagorin@gmail.com)',
        anchor: 'center',
    }]
});
