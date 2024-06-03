import React, { useState } from "react";
import ReactModal from "react-modal";
import "./AddReviewModal.css";

function AddReviewModal({ isOpen, onRequestClose, onReviewSubmit }) {
  // Define fields for review
  const [username, setUsername] = useState("");
  const [wheelchairAccessRating, setWheelchairAccessRating] = useState(0);
  const [restroomRating, setRestroomRating] = useState(0);
  const [overallRating, setOverallRating] = useState(0);
  const [comments, setComments] = useState("");

  const submitReview = () => {
    // Handle the submission logic here
    onReviewSubmit({
      username: username,
      wheelchairRating: wheelchairAccessRating,
      restroomRating: restroomRating,
      overallRating: overallRating,
      comments: comments,
    });

    // Reset form
    setUsername("");
    setWheelchairAccessRating(0);
    setRestroomRating(0);
    setOverallRating(0);
    setComments("");
    onRequestClose(); // Close the modal
  };

  return (
    <ReactModal
      isOpen={isOpen}
      onRequestClose={onRequestClose}
      contentLabel="Add Review Modal"
      className="add-review-modal"
      overlayClassName="Overlay"
    >
      <h2>Add Review</h2>
      <form onSubmit={submitReview}>
        {" "}
        <div className="form-field">
          <label htmlFor="username">Username:</label>
          <input
            id="username"
            type="text"
            placeholder="Your username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>
        <div className="form-field">
          <label htmlFor="wheelchairAccess">Wheelchair Access:</label>
          <select
            id="wheelchairAccess"
            value={wheelchairAccessRating}
            onChange={(e) => setWheelchairAccessRating(e.target.value)}
          >
            <option value="0">Select rating</option>
            {[1, 2, 3, 4, 5].map((rating) => (
              <option key={rating} value={rating}>
                {rating}
              </option>
            ))}
          </select>
        </div>
        <div className="form-field">
          <label htmlFor="restroomAccess">Restroom Access:</label>
          <select
            id="restroomAccess"
            value={restroomRating}
            onChange={(e) => setRestroomRating(e.target.value)}
          >
            <option value="0">Select rating</option>
            {[1, 2, 3, 4, 5].map((rating) => (
              <option key={rating} value={rating}>
                {rating}
              </option>
            ))}
          </select>
        </div>
        <div className="form-field">
          <label htmlFor="overallRating">Overall:</label>
          <select
            id="overallRating"
            value={overallRating}
            onChange={(e) => setOverallRating(e.target.value)}
          >
            <option value="0">Select rating</option>
            {[1, 2, 3, 4, 5].map((rating) => (
              <option key={rating} value={rating}>
                {rating}
              </option>
            ))}
          </select>
        </div>
        <div className="form-field">
          <label htmlFor="comments">Comments:</label>
          <textarea
            id="comments"
            placeholder="Tell us more about your experience"
            value={comments}
            onChange={(e) => setComments(e.target.value)}
          />
        </div>
        <div className="form-actions">
          <button type="button" onClick={onRequestClose}>
            Cancel
          </button>
          <button type="submit">Submit</button>{" "}
          {/* Changed from onClick to type="submit" */}
        </div>
      </form>
    </ReactModal>
  );
}

export default AddReviewModal;
