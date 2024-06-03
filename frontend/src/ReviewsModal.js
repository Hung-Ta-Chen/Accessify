import React from "react";
import ReactModal from "react-modal";
import "./ReviewsModal.css";

function ReviewsModal({ isOpen, onRequestClose, reviews }) {
  return (
    <ReactModal
      isOpen={isOpen}
      onRequestClose={onRequestClose}
      contentLabel="Reviews"
      overlayClassName="ReviewsModal__Overlay"
      className="ReviewsModal__Content"
    >
      <div className="reviews-modal-content">
        <button onClick={onRequestClose}>
          {" "}
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
        <h2>Reviews</h2>
        <div className="reviews-list">
          {reviews.map((review, index) => (
            <div className="review" key={index}>
              <div className="review-header">
                <p className="username">Username: {review.username}</p>
                <p className="ratings">
                  Wheelchair: {review.wheelchair_rating} Stars
                </p>
                <p className="ratings">
                  Restroom: {review.restroom_rating} Stars
                </p>
                <p className="ratings">
                  Overall: {review.overall_rating} Stars
                </p>
              </div>
              <p className="comments">Comment: {review.comment}</p>
            </div>
          ))}
        </div>
      </div>
    </ReactModal>
  );
}

export default ReviewsModal;
