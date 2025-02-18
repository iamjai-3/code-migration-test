const items = require("../data/items");

exports.getItems = (req, res) => {
  const { id } = req.params;
  if (id) {
    if (items[id]) {
      res.json(items[id]);
    } else {
      res.status(404).json({ message: "Item not found" });
    }
  } else {
    res.json(Object.values(items));
  }
};

exports.createItem = (req, res) => {
  const { name, description } = req.body;
  const id = Object.keys(items).length + 1;
  items[id] = { id, name, description };
  res.status(201).json(items[id]);
};

exports.updateItem = (req, res) => {
  const { id } = req.params;
  const { name, description } = req.body;

  if (!items[id]) {
    return res.status(404).json({ message: "Item not found" });
  }

  items[id] = {
    ...items[id],
    name: name || items[id].name,
    description: description || items[id].description,
  };

  res.json(items[id]);
};

exports.deleteItem = (req, res) => {
  const { id } = req.params;

  if (!items[id]) {
    return res.status(404).json({ message: "Item not found" });
  }

  delete items[id];
  res.json({ message: "Item deleted" });
};
