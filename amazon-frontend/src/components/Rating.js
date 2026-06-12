import React from 'react'
import StarIcon from '@mui/icons-material/Star';
import StarBorderIcon from '@mui/icons-material/StarBorder';
import StarHalfIcon from '@mui/icons-material/StarHalf';
import "../styles/Rating.css"
import Product from './Product';


const Rating = (props) => {
    
    const {rating, numRev} = props;

    return (
        <div className="rating-container">

            <div className="rating">
                { (rating>=1)
                ? <StarIcon/>
                : (rating === 0.5)
                ? <StarHalfIcon/>
                : <StarBorderIcon/>
                }

                { (rating>=2)
                ? <StarIcon/>
                : (rating === 1.5)
                ? <StarHalfIcon/>
                : <StarBorderIcon/>
                }

                { (rating>=3)
                ? <StarIcon/>
                : (rating === 2.5)
                ? <StarHalfIcon/>
                : <StarBorderIcon/>
                }

                { (rating>=4)
                ? <StarIcon/>
                : (rating === 3.5)
                ? <StarHalfIcon/>
                : <StarBorderIcon/>
                }

                { (rating===5)
                ? <StarIcon/>
                : (rating === 4.5)
                ? <StarHalfIcon/>
                : <StarBorderIcon/>
                }
            </div>

            <span>{numRev} reviews</span>


        </div>
        
    )
}

export default Rating
