from sqlalchemy import Integer, Column, String, create_engine, ForeignKey, Text
from sqlalchemy.orm import sessionmaker, declarative_base
from fastapi.encoders import jsonable_encoder


class DbServer:
    __engine = create_engine("sqlite:///data.db")
    __Base = declarative_base()
    Session = sessionmaker(__engine)

    class Novel(__Base):
        __tablename__ = "Novel"
        nid = Column(Integer, primary_key=True, autoincrement=True)
        title = Column(String, nullable=False)
        desc = Column(String, nullable=True)
        author = Column(String, nullable=True)
        img = Column(String, nullable=True)

    class Chapter(__Base):
        __tablename__ = "Chapter"
        nid = Column(Integer, ForeignKey("Novel.nid"), nullable=False)
        cid = Column(Integer, primary_key=True, autoincrement=True)  # 0 1 2 3 偏移
        title = Column(Text)
        content = Column(Text)

    
    class Character(__Base):
        __tablename__ = "Character"
        chid = Column(Integer, primary_key=True, autoincrement=True)
        name = Column(String, nullable=False)
        voice = Column(String, nullable=False)
        desc = Column(String, nullable=True)
        img = Column(String, nullable=True)
        

    def __init__(self):
        try:
            self.__Base.metadata.create_all(self.__engine)
        except:
            pass

    def new_novel(self, title: str, desc: str = None, author: str = None, img: str = None) -> int:
        session = self.Session()
        try:
            novel = self.Novel(title=title, desc=desc, author=author, img=img)

            session.add(novel)
            session.commit()
            session.flush()

            return novel.nid

        except Exception as e:
            session.rollback()
            raise e

        finally:
            session.close()

    def new_chapter(self, nid: int, title: str, content: str, cid: int = None) -> int:
        session = self.Session()
        try:
            if not cid:
                chapter = self.Chapter(nid=nid, title=title, content=content)
            else:
                chapter = self.Chapter(nid=nid, title=title, content=content, cid=cid)

            session.add(chapter)
            session.commit()
            session.flush()

            return chapter.cid

        except Exception as e:
            session.rollback()
            raise e

        finally:
            session.close()

    def update_chapter(self, nid: int, cid: int, content: str) -> int:
        session = self.Session()
        try:
            chapter = (
                session.query(self.Chapter)
                .filter(self.Chapter.nid == nid and self.Chapter.cid == cid)
                .first()
            )
            chapter.content = content
            session.add(chapter)
            session.commit()

        except Exception as e:
            session.rollback()
            raise e

        finally:
            session.close()

    def query_novel_list(self):
        session = self.Session()
        try:
            return jsonable_encoder(session.query(self.Novel).all())
        except Exception as e:
            raise e 
        finally:
            session.close()


    def query_single_novel(self, nid:int):
        session = self.Session()
        try:
            return jsonable_encoder(
                session.query(
                    self.Novel
                )
                .filter(self.Novel.nid == nid)
                .first()
            )
        except Exception as e:
            raise e
        finally:
            session.close()

    def query_chapter_list(self, nid: int):
        session = self.Session()
        try:
            tp_lst:list[tuple] = session.query(
                    self.Chapter.cid,
                    self.Chapter.title,
                )\
                .filter(self.Chapter.nid == nid)\
                .all()

            tp_lst.sort()

            return [{'cid': tp[0], 'title': tp[1]} for tp in tp_lst]
        except Exception as e:
            raise e
        finally:
            session.close()

    def query_single_chapter(self, nid: int, cid: int):
        session = self.Session()
        try:
            tp = session.query(
                    self.Chapter.title,
                    self.Chapter.content
                )\
                .filter(self.Chapter.nid == nid and self.Chapter.cid == cid)\
                .first()

            return {'title': tp[0], 'content': tp[1]}

        except Exception as e:
            raise e
        finally:
            session.close()

    def new_character(self, name: str, voice: str, desc: str|None = None, img: str|None = None):
        session = self.Session()
        try:
            
            character = self.Character(name=name, voice=voice, desc=desc, img=img)

            session.add(character)
            session.commit()
            session.flush()

            return character.chid

        except Exception as e:
            session.rollback()
            raise e

        finally:
            session.close()
        
    def delete_character(self, chid: int) -> int:
        session = self.Session()
        try:
            session.query(self.Character)\
                .filter(self.Character.chid == chid)\
                .delete(synchronize_session='fetch')
        
            session.commit()

        except Exception as e:
            session.rollback()
            raise e

        finally:
            session.close()

    def query_characters(self):
        session = self.Session()
        try:
            return jsonable_encoder(session.query(self.Character).all())
        except Exception as e:
            raise e 
        finally:
            session.close()
    