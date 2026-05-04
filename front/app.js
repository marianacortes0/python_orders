require('dotenv').config();
const express = require('express');
const path = require('path');
const methodOverride = require('method-override');
const routes = require('./src/routes');

const app = express();
const PORT = process.env.PORT || 3001;

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(methodOverride('_method'));

// Servir DevExtreme desde node_modules
app.use('/dx/css', express.static(path.join(__dirname, 'node_modules/devextreme/dist/css')));
app.use('/dx/js',  express.static(path.join(__dirname, 'node_modules/devextreme/bundles')));
app.use('/dx/icons', express.static(path.join(__dirname, 'node_modules/devextreme/dist/css/icons')));
app.use('/dx/fonts', express.static(path.join(__dirname, 'node_modules/devextreme/dist/css/fonts')));

app.use(express.static(path.join(__dirname, 'public')));

app.use('/', routes);

app.use((req, res) => {
  res.status(404).render('error', { title: 'Página no encontrada', message: 'La página solicitada no existe.' });
});

app.use((err, req, res, _next) => {
  console.error(err.stack);
  res.status(500).render('error', { title: 'Error interno', message: err.message });
});

app.listen(PORT, () => {
  console.log(`Frontend corriendo en http://localhost:${PORT}`);
});

module.exports = app;
