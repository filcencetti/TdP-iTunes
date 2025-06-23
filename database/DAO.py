from database.DB_connect import DBConnect
from model.album import Album


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllAlbums(l):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
               select distinct a.AlbumId, a.Title, a.ArtistId, sum(t.Milliseconds/60000) as Lenght
                from album a, track t
                where a.AlbumId = t.AlbumId
                group by a.AlbumId, a.Title, a.ArtistId
                having sum(t.Milliseconds/60000) > %s
                        """
        cursor.execute(query,(l,))

        for row in cursor:
            result.append(Album(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges(idMap):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor()
        query = """
                select t1.AlbumId, t2.AlbumId
                from playlisttrack p1, playlisttrack p2, track t1, track t2
                where p1.TrackId = t1.TrackId
                and p2.TrackId = t2.TrackId
                and p1.PlaylistId = p2.PlaylistId
                and t1.AlbumId < t2.AlbumId
                group by t1.AlbumId, t2.AlbumId
                """
        cursor.execute(query)

        for row in cursor:
            if row[0] in idMap.keys() and row[1] in idMap.keys():
                result.append(row)

        cursor.close()
        conn.close()
        return result