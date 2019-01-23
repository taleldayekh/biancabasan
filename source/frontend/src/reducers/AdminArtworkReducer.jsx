const defaultState = {
    artworkObjectId: "",
    title: "",
    yearFrom: "",
    yearTo: "",
    material: "",
    height: "",
    width: "",
    depth: "",
    description: "",
    imageList: null
}

const Artwork = (state = defaultState, action) => {
    switch (action.type) {
        case 'ADD_ID':
            return state = {
                ...state,
                artworkObjectId: action.payload
            };
        case 'SET_TITLE':
            return state = {
                ...state,
                title: action.payload
            };
        case 'SET_YEAR_FROM':
            return state = {
                ...state,
                yearFrom: action.payload
            };
        case 'SET_YEAR_TO':
            return state = {
                ...state,
                yearTo: action.payload
            };
        case 'SET_MATERIAL':
            return state = {
                ...state,
                material: action.payload
            };
        case 'SET_HEIGHT':
            return state = {
                ...state,
                height: action.payload
            };
        case 'SET_WIDTH':
            return state = {
                ...state,
                width: action.payload
            };
        case 'SET_DEPTH':
            return state = {
                ...state,
                depth: action.payload
            };
        case 'SET_DESCRIPTION':
            return state = {
                ...state,
                description: action.payload
            };
        case 'UPLOAD_IMAGES':
            return state = {
                ...state,
                imageList: action.payload
            }
        default:
            return state;
    }
}


export default Artwork;