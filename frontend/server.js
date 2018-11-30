'use strict';

const http = require('http');
const express = require('express');
const PORT = 8080;
const HOST = '0.0.0.0';
const app = express();
const path = __dirname + '/views'
app.set('view engine', 'ejs');

function generate_tree_data(branch_in_data, branch_in_result, parent) {
    for (var key in branch_in_data) {
        var node = {"name": key, "parent": parent};
        var deps = branch_in_data[key];
        if (Object.keys(deps).length > 0) {
            var children = [];
            node["children"] = children;
            generate_tree_data(branch_in_data[key], children, parent)
        }
        branch_in_result.push(node);
    }
}

function on_end(body, res) {
    var data = JSON.parse(body);
    var treeData = [];
    var root_key = Object.keys(data)[0];
    var root_deps = data[root_key];
    var root_node = { "name": root_key, "parent": null };

    treeData.push(root_node);
    if (Object.keys(root_deps).length === 0) {
        res.render(path + '/index.ejs', { "treeData": treeData });
        return;
    }
    var root_children = [];
    root_node["children"] = root_children;
    generate_tree_data(data[root_key], treeData[0]["children"], root_key);
    res.render(path + '/index.ejs', { "treeData": treeData });
}

app.get('/:pkg/:version', (req, res) => {
    const pkg = req.params.pkg;
    const version = req.params.version;
    const options = {
        host: 'api-' + Math.floor(Math.random() * Math.floor(3)).toString(),
        port: PORT,
        path: '/api/' + pkg + '/' + version,
        method: 'GET',
        json: true
    };
    http.get(options, function (_res) {
        console.log(res.statusCode);
        var body = "";
        _res.on('data', function (chunk) {
            // You can process streamed parts here...
            body += chunk;
        }).on('end', function () {
            on_end(body, res)
        })
    });
});

app.get('/ping', (req, res) => {
    res.send('pong')
});

app.listen(PORT, HOST);
