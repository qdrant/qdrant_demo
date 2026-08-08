import { Axios } from "./axios";
import { SEARCH_URL } from "./constants";


export type SearchMode = "semantic" | "keyword" | "hybrid";

export type SearchRequest = {
    query: string;
    mode?: SearchMode;
}

export const getSearchResult = (searchRequest: SearchRequest) => {
    const params = {
        q: searchRequest.query,
        mode: searchRequest.mode ?? "hybrid",
    }
    return Axios().get(SEARCH_URL, { params });
};
