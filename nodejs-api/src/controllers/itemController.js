const data = require("../data/data");

const getItems = (req, res) => {
  const { id } = req.params;
  if (id) {
    if (data[id]) {
      res.json(data[id]);
    } else {
      res.status(404).json({ message: "Item not found" });
    }
  } else {
    res.json(Object.values(data));
  }
};

module.exports = { getItems };

const createItem = (req, res) => {
  const { name, description } = req.body;
  const id = Object.keys(data).length + 1;
  data[id] = {
    id,
    name,
    description,
  };
  res.status(201).json(data[id]);
};

module.exports = { getItems, createItem };

const updateItem = (req, res) => {
  const { id } = req.params;
  if (!data[id]) {
    return res.status(404).json({ message: "Item not found" });
  }
  data[id] = {
    ...data[id],
    ...req.body,
  };
  res.json(data[id]);
};

module.exports = { getItems, createItem, updateItem };

const deleteItem = (req, res) => {
  const { id } = req.params;
  if (!data[id]) {
    return res.status(404).json({ message: "Item not found" });
  }
  delete data[id];
  res.json({ message: "Item deleted" });
};

module.exports = { getItems, createItem, updateItem, deleteItem };
