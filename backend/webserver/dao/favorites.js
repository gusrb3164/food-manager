class Favorites {}

require('../utils/dbconnector')(Favorites);

Favorites.getFavoritesByUserId = async (userId) => {
    // score = 1 인 값(좋아요) 만 가져옴
    const [row, fields] = await Favorites.db.execute("SELECT id, name, favorite_id, score FROM recipes r JOIN ( SELECT id as favorite_id, recipe_id,score FROM favorites WHERE user_id=? AND score=1) f ON r.id = f.recipe_id", [userId]);
	return row;
}

Favorites.insertFavorite = async (userId, recipeId, score) => {
    await Favorites.db.execute("INSERT INTO favorites(user_id, recipe_id, score) VALUES(?,?,?)", [userId, recipeId, score]);
}

Favorites.deleteFavorite = async (userId, recipeId) => {
	await Favorites.db.execute("DELETE FROM favorites WHERE user_id=? AND recipe_id=?", [userId, recipeId]);
}

module.exports = Favorites;
