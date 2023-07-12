const $delbtn = $(".delete");

$delbtn.on("click", async function (e) {
	e.preventDefault();
	if (confirm("Are you sure you want to delete this post?")) {
		let $parent = $(this).parent();
		let parentId = $parent.attr("data-feedback-id");
		await axios.post(`/feedback/${parentId}/delete`);
		$parent.remove();
		console.log("deleted");
	} else {
		console.log("Canceled");
	}
});
